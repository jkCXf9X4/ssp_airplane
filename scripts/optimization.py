#!/usr/bin/env python3
"""Optimize wing area, motor size, and payload while checking program requirements."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable

try:  # pragma: no cover - optional OMSimulator bindings
    import OMSimulator as oms  # type: ignore
except ModuleNotFoundError:  # noqa: SIM105
    try:
        import oms  # type: ignore
    except ModuleNotFoundError:
        oms = None  # type: ignore

from sysml_loader import load_architecture

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCH_PATH = REPO_ROOT / "architecture" / "aircraft_architecture.sysml"
DEFAULT_REPORT = REPO_ROOT / "build" / "reports" / "optimization_result.json"
LONDON_BEIJING_KM = 8140


@dataclass
class OptimizationResult:
    wing_area_scale: float
    engine_thrust_scale: float
    payload_scale: float
    estimated_range_km: float
    thrust_margin: float
    payload_capacity_kg: float
    objective: float


@dataclass
class VerificationStatus:
    size_within_bounds: bool
    propulsion_is_conventional: bool
    range_requirement_met: bool
    notes: str


def get_component(data: dict, name: str) -> dict:
    for comp in data.get("components", []):
        if comp["name"] == name:
            return comp
    raise KeyError(f"Component '{name}' not defined in architecture")


def evaluate_design(
    wing_scale: float,
    engine_scale: float,
    payload_scale: float,
    arch: dict,
) -> OptimizationResult:
    analysis = arch.get("analysis_parameters", {})
    base_range = float(analysis.get("target_range_km", 8000))
    payload_base = float(get_component(arch, "CompositeAirframe")["parameters"]["payload_capacity_kg"])
    payload_capacity = payload_base * payload_scale

    aerodynamic_gain = 0.85 + 0.35 * wing_scale
    propulsion_gain = 0.75 + 0.45 * engine_scale
    payload_penalty = 0.35 + 0.35 * payload_scale

    estimated_range = base_range * aerodynamic_gain * propulsion_gain / payload_penalty
    thrust_margin = propulsion_gain / payload_penalty
    objective = estimated_range - 0.0005 * payload_capacity

    return OptimizationResult(
        wing_area_scale=wing_scale,
        engine_thrust_scale=engine_scale,
        payload_scale=payload_scale,
        estimated_range_km=estimated_range,
        thrust_margin=thrust_margin,
        payload_capacity_kg=payload_capacity,
        objective=objective,
    )


def linspace(bounds: tuple[float, float], samples: int) -> Iterable[float]:
    start, stop = bounds
    if samples <= 1 or abs(stop - start) < 1e-9:
        yield float(start)
        return
    step = (stop - start) / (samples - 1)
    for idx in range(samples):
        yield float(start + idx * step)


def run_grid_search(arch: dict, samples: int) -> OptimizationResult:
    vars_cfg = arch.get("analysis_parameters", {}).get("optimization_variables", [])
    bounds = {var["name"]: (var["min"], var["max"]) for var in vars_cfg}
    wing_bounds = bounds.get("wing_area_scale", (0.8, 1.2))
    engine_bounds = bounds.get("engine_thrust_scale", bounds.get("motor_power_scale", (0.7, 1.3)))
    payload_bounds = bounds.get("payload_scale", (0.6, 1.1))

    best: OptimizationResult | None = None
    for wing in linspace(wing_bounds, samples):
        for engine in linspace(engine_bounds, samples):
            for payload in linspace(payload_bounds, samples):
                candidate = evaluate_design(float(wing), float(engine), float(payload), arch)
                if candidate.estimated_range_km < LONDON_BEIJING_KM:
                    continue
                if best is None or candidate.objective > best.objective:
                    best = candidate
    if not best:
        best = evaluate_design(wing_bounds[1], engine_bounds[1], payload_bounds[0], arch)
    return best


def verify_requirements(arch: dict, result: OptimizationResult) -> VerificationStatus:
    airframe = get_component(arch, "CompositeAirframe")
    wings = get_component(arch, "AdaptiveWingSystem")
    propulsion = get_component(arch, "TurbofanPropulsion")

    size_ok = (
        abs(float(airframe["parameters"]["length_m"]) - 11.7) <= 0.6
        and abs(float(wings["parameters"]["span_m"]) - 7.3) <= 0.5
    )
    propulsion_ok = float(propulsion["parameters"]["max_thrust_kn"]) > 0
    range_ok = result.estimated_range_km >= LONDON_BEIJING_KM

    notes = "Range satisfied" if range_ok else "Adjust thrust/fuel/payload mix"
    return VerificationStatus(size_ok, propulsion_ok, range_ok, notes)


def refine_with_oms(ssp_path: Path | None, result: OptimizationResult) -> None:
    if ssp_path is None:
        return
    if oms is None:
        print("[warn] OMSimulator python package unavailable; skipping SSP co-simulation")
        return
    if not ssp_path.exists():
        print(f"[warn] SSP file {ssp_path} not found; skipping OMS co-simulation")
        return

    model = None
    try:
        import_response = oms.importFile(str(ssp_path))
        model = import_response[1] if isinstance(import_response, tuple) else import_response
        param_prefix = f"{model}.root.DroneSystem"
        for name, value in (
            ("wingAreaScale", result.wing_area_scale),
            ("engineThrustScale", result.engine_thrust_scale),
            ("payloadScale", result.payload_scale),
        ):
            try:
                oms.setReal(f"{param_prefix}.{name}", value)
            except Exception:  # noqa: BLE001
                pass

        oms.instantiate(model)
        oms.initialize(model)
        oms.simulate(model)
        try:
            response = oms.getReal(f"{param_prefix}.rangeEstimateKm")
            range_value = response[-1] if isinstance(response, tuple) else response
            result.estimated_range_km = float(range_value)
        except Exception:  # noqa: BLE001
            pass
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] OMS co-simulation failed: {exc}")
    finally:
        if model:
            try:
                oms.terminate(model)
                oms.delete(model)
            except Exception:
                pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=ARCH_PATH)
    parser.add_argument("--samples", type=int, default=5, help="Samples per dimension for grid search")
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--ssp", type=Path, default=None, help="Optional SSP archive for OMSimulator refinement")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    arch = load_architecture(args.architecture)
    result = run_grid_search(arch, args.samples)
    refine_with_oms(args.ssp, result)
    verification = verify_requirements(arch, result)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload: Dict[str, Any] = {
        "optimization": asdict(result),
        "verification": asdict(verification),
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
