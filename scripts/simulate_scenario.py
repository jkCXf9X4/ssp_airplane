#!/usr/bin/env python3
"""Simulate a waypoint scenario with OMSimulator or an analytic dry-run."""
from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
THIRD_PARTY = REPO_ROOT / "third_party"
DEFAULT_SSP = REPO_ROOT / "build" / "ssp" / "wingman_drone.ssp"
DEFAULT_RESULTS = REPO_ROOT / "build" / "results"
DESIGN_RANGE_KM = 3700.0


def ensure_third_party_on_path() -> None:
    if THIRD_PARTY.exists() and str(THIRD_PARTY) not in sys.path:
        sys.path.insert(0, str(THIRD_PARTY))


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def haversine_distance_km(points: List[Dict[str, float]]) -> float:
    def radians(point: Dict[str, float]) -> tuple[float, float]:
        return math.radians(point["latitude_deg"]), math.radians(point["longitude_deg"])

    total = 0.0
    for i in range(len(points) - 1):
        lat1, lon1 = radians(points[i])
        lat2, lon2 = radians(points[i + 1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        total += 2 * 6371.0 * math.asin(min(1.0, math.sqrt(h)))
    return total


def estimate_duration(distance_km: float, cruise_speed_mps: float) -> float:
    return max(60.0, (distance_km * 1000.0) / max(1.0, cruise_speed_mps))


@dataclass
class ScenarioResult:
    scenario_path: Path
    total_distance_km: float
    estimated_duration_s: float
    fuel_capacity_kg: float
    fuel_burn_rate_kgps: float
    fuel_required_kg: float
    fuel_exhausted: bool
    meets_range_requirement: bool
    used_oms: bool
    result_file: Optional[Path]


def run_with_oms(ssp_path: Path, result_file: Path, stop_time: float) -> None:
    ensure_third_party_on_path()
    try:
        from OMSimulator import OMSimulator  # type: ignore
    except ImportError as exc:  # pragma: no cover - dependent on environment
        raise SystemExit(
            "OMSimulator Python package not available. Install it locally or via pip."
        ) from exc

    api = OMSimulator()
    api.setCommandLineOption("--suppressPath=true")
    temp_dir = Path(tempfile.mkdtemp(prefix="oms_run_"))
    api.setTempDirectory(str(temp_dir))

    model_name = api.importFile(str(ssp_path))
    if not model_name:
        raise RuntimeError(f"OMSimulator failed to import SSP: {ssp_path}")

    api.setResultFile(model_name, str(result_file))
    api.setStopTime(model_name, stop_time)
    api.instantiate(model_name)
    api.initialize(model_name)
    api.simulate(model_name)
    api.terminate(model_name)
    api.delete(model_name)


def simulate_scenario(
    scenario_path: Path,
    ssp_path: Optional[Path] = None,
    results_dir: Path = DEFAULT_RESULTS,
    use_oms: bool = True,
    cruise_speed_mps: float = 250.0,
    fuel_capacity_kg: float = 2000.0,
    fuel_burn_rate_kgps: float = 0.55,
) -> ScenarioResult:
    scenario = load_json(scenario_path)
    if "points" not in scenario:
        raise ValueError("Scenario file must contain a 'points' list.")

    total_distance = scenario.get("total_distance_km") or haversine_distance_km(scenario["points"])
    duration_s = estimate_duration(total_distance, cruise_speed_mps)
    fuel_required = duration_s * fuel_burn_rate_kgps
    fuel_exhausted = fuel_required > fuel_capacity_kg
    meets_range = total_distance <= DESIGN_RANGE_KM

    result_file: Optional[Path] = None
    used_oms_flag = False
    if use_oms:
        if not ssp_path:
            ssp_path = DEFAULT_SSP
        if not ssp_path.exists():
            raise FileNotFoundError(f"SSP file not found: {ssp_path}")
        results_dir.mkdir(parents=True, exist_ok=True)
        result_file = results_dir / f"{scenario_path.stem}_results.csv"
        run_with_oms(ssp_path, result_file, stop_time=duration_s)
        used_oms_flag = True

    return ScenarioResult(
        scenario_path=scenario_path,
        total_distance_km=total_distance,
        estimated_duration_s=duration_s,
        fuel_capacity_kg=fuel_capacity_kg,
        fuel_burn_rate_kgps=fuel_burn_rate_kgps,
        fuel_required_kg=fuel_required,
        fuel_exhausted=fuel_exhausted,
        meets_range_requirement=meets_range,
        used_oms=used_oms_flag,
        result_file=result_file,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, required=True, help="Path to scenario JSON file.")
    parser.add_argument("--ssp", type=Path, default=None, help="Path to the SSP archive.")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--cruise-speed", type=float, default=250.0, help="Cruise speed in m/s.")
    parser.add_argument("--fuel-capacity", type=float, default=2000.0, help="Fuel capacity in kg.")
    parser.add_argument("--fuel-burn-rate", type=float, default=0.55, help="Average fuel burn in kg/s.")
    parser.add_argument("--dry-run", action="store_true", help="Skip OMSimulator execution.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = simulate_scenario(
        scenario_path=args.scenario,
        ssp_path=args.ssp,
        results_dir=args.results_dir,
        use_oms=not args.dry_run,
        cruise_speed_mps=args.cruise_speed,
        fuel_capacity_kg=args.fuel_capacity,
        fuel_burn_rate_kgps=args.fuel_burn_rate,
    )
    print(
        json.dumps(
            {
                "scenario": str(result.scenario_path),
                "distance_km": round(result.total_distance_km, 2),
                "duration_s": round(result.estimated_duration_s, 1),
                "fuel_required_kg": round(result.fuel_required_kg, 1),
                "fuel_exhausted": result.fuel_exhausted,
                "meets_range_requirement": result.meets_range_requirement,
                "used_oms": result.used_oms,
                "result_file": str(result.result_file) if result.result_file else None,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
