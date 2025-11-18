#!/usr/bin/env python3
"""Simulate a waypoint scenario with OMSimulator and post-process the results."""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
import xml.etree.ElementTree as ET

# activate venv prior
import pyssp4sim
import matplotlib

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SSP = REPO_ROOT / "build" / "ssp" / "aircraft.ssp"
DEFAULT_RESULTS = REPO_ROOT / "build" / "results"
DEFAULT_FUEL_CAPACITY = 3100.0
RESERVE_FRACTION = 0.08
WAYPOINT_HIT_THRESHOLD_KM = 10.0


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
        h = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        total += 2 * 6371.0 * math.asin(min(1.0, math.sqrt(h)))
    return total


def estimate_duration(distance_km: float, cruise_speed_mps: float) -> float:
    return max(60.0, (distance_km * 1000.0) / max(1.0, cruise_speed_mps))


def local_path_distance_km(points: List[Dict[str, float]]) -> float:
    total = 0.0
    for i in range(len(points) - 1):
        dx = points[i + 1]["x_km"] - points[i]["x_km"]
        dy = points[i + 1]["y_km"] - points[i]["y_km"]
        dz = points[i + 1].get("z_km", 0.0) - points[i].get("z_km", 0.0)
        total += math.sqrt(dx * dx + dy * dy + dz * dz)
    return total


def _numeric_series(
    rows: Sequence[Dict[str, str]], key: str, cast=float
) -> List[float]:
    values: List[float] = []
    for row in rows:
        raw = row.get(key, "")
        if raw is None:
            continue
        raw_str = str(raw).strip()
        if not raw_str:
            continue
        try:
            values.append(cast(raw_str))
        except ValueError:
            try:
                values.append(cast(raw_str.replace(",", "")))
            except ValueError:
                continue
    return values


def _span(values: Sequence[float]) -> float:
    return max(values) - min(values) if values else 0.0


def _read_result_rows(result_file: Path) -> List[Dict[str, str]]:
    with result_file.open() as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def scenario_to_string(points: List[Dict[str, float]]) -> str:
    """Serialize local waypoint points [{x_km,y_km,z_km}] into csv string."""
    values: List[str] = []
    for point in points:
        values.append(f"{point['x_km']:.3f}")
        values.append(f"{point['y_km']:.3f}")
        values.append(f"{point.get('z_km', 0.0):.3f}")
    return ",".join(values)


def validate_scenario_points(points: List[Dict[str, float]]) -> None:
    for idx, point in enumerate(points):
        if "latitude_deg" not in point or "longitude_deg" not in point:
            raise ValueError(f"Point {idx} missing latitude or longitude")
        lat = float(point["latitude_deg"])
        lon = float(point["longitude_deg"])
        if not -90.0 <= lat <= 90.0 or not -180.0 <= lon <= 180.0:
            raise ValueError(f"Point {idx} has implausible lat/lon: {lat}, {lon}")
        if "altitude_m" in point:
            alt = float(point["altitude_m"])
            if alt < -500 or alt > 25000:
                raise ValueError(f"Point {idx} has implausible altitude: {alt}")


def project_waypoints_to_local_km(points: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """Convert geodetic waypoints to a local x/y/z frame in kilometers relative to the first point."""
    if not points:
        return []
    origin = points[0]
    lat0 = float(origin["latitude_deg"])
    lon0 = float(origin["longitude_deg"])
    lat0_rad = math.radians(lat0)
    projected: List[Dict[str, float]] = []
    for point in points:
        lat = float(point["latitude_deg"])
        lon = float(point["longitude_deg"])
        alt_m = float(point.get("altitude_m", 0.0))
        x_km = 111.0 * (lat - lat0)
        y_km = 111.0 * math.cos(lat0_rad) * (lon - lon0)
        projected.append({"x_km": x_km, "y_km": y_km, "z_km": alt_m / 1000.0})
    return projected


def extract_track_points(
    rows: List[Dict[str, str]],
) -> List[Tuple[float, float, float]]:
    xs = _numeric_series(rows, "Environment.location.x_km") or _numeric_series(
        rows, "MissionComputer.locationXYZ.x_km"
    )
    ys = _numeric_series(rows, "Environment.location.y_km") or _numeric_series(
        rows, "MissionComputer.locationXYZ.y_km"
    )
    zs = _numeric_series(rows, "Environment.location.z_km") or _numeric_series(
        rows, "MissionComputer.locationXYZ.z_km"
    )

    # Backward-compatibility for legacy lat/lon recordings in existing CSVs
    if (not xs or not ys) and _numeric_series(rows, "MissionComputer.locationLLA.latitude_deg"):
        lats = _numeric_series(rows, "MissionComputer.locationLLA.latitude_deg")
        lons = _numeric_series(rows, "MissionComputer.locationLLA.longitude_deg")
        alts_m = _numeric_series(rows, "MissionComputer.locationLLA.altitude_m")
        if lats and lons:
            lat0 = lats[0]
            lon0 = lons[0]
            lat0_rad = math.radians(lat0)
            xs = [111.0 * (lat - lat0) for lat in lats]
            ys = [111.0 * math.cos(lat0_rad) * (lon - lon0) for lon in lons]
            zs = [alt / 1000.0 for alt in alts_m] if alts_m else [0.0 for _ in lats]

    n = min(len(xs), len(ys), len(zs))
    return [(xs[i], ys[i], zs[i]) for i in range(n)]


def plot_flight_path(
    result_file: Path, scenario_points: List[Dict[str, float]], output_path: Path
) -> Optional[Path]:
    import os

    if os.getenv("SIM_SKIP_PLOTS") == "1":
        return None

    try:
        
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None

    rows = _read_result_rows(result_file)
    xs = _numeric_series(rows, "Environment.location.x_km")
    ys = _numeric_series(rows, "Environment.location.y_km")

    if (not xs or not ys) and _numeric_series(rows, "MissionComputer.locationLLA.latitude_deg"):
        lats = _numeric_series(rows, "MissionComputer.locationLLA.latitude_deg")
        lons = _numeric_series(rows, "MissionComputer.locationLLA.longitude_deg")
        if lats and lons:
            lat0 = lats[0]
            lon0 = lons[0]
            lat0_rad = math.radians(lat0)
            xs = [111.0 * (lat - lat0) for lat in lats]
            ys = [111.0 * math.cos(lat0_rad) * (lon - lon0) for lon in lons]

    if not xs or not ys:
        return None

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(xs, ys, label="Flight path", color="#1f77b4")

    if scenario_points:
        wp_x = [p["x_km"] for p in scenario_points]
        wp_y = [p["y_km"] for p in scenario_points]
        ax.plot(wp_x, wp_y, "o--", label="Waypoints", color="#d62728")

    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_title("Flight path vs waypoints (local frame)")
    ax.legend()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def waypoint_tracking_metrics(
    scenario_points: List[Dict[str, float]],
    track_points: List[Tuple[float, float, float]],
    threshold_km: float = WAYPOINT_HIT_THRESHOLD_KM,
) -> Dict[str, float]:
    if not scenario_points or not track_points:
        return {
            "waypoint_miss_max_km": float("nan"),
            "waypoint_miss_avg_km": float("nan"),
            "waypoint_hits": 0,
            "waypoint_total": len(scenario_points),
            "waypoint_within_threshold_fraction": 0.0,
        }

    misses: List[float] = []
    hits = 0
    for wp in scenario_points:
        x = float(wp["x_km"])
        y = float(wp["y_km"])
        best = min(math.sqrt((x - t[0]) ** 2 + (y - t[1]) ** 2) for t in track_points)
        misses.append(best)
        if best <= threshold_km:
            hits += 1

    total = len(scenario_points)
    return {
        "waypoint_miss_max_km": max(misses),
        "waypoint_miss_avg_km": sum(misses) / total if total else float("nan"),
        "waypoint_hits": hits,
        "waypoint_total": total,
        "waypoint_within_threshold_fraction": hits / total if total else 0.0,
        "waypoints_followed": 1.0 if total and hits == total else 0.0,
    }


def emit_waypoint_parameter_set(
    local_points: List[Dict[str, float]],
    output_path: Path,
    component: str = "AutopilotModule",
) -> Path:
    ns = "http://ssp-standard.org/SSP1/ParameterValues"
    ET.register_namespace("ssv", ns)
    root = ET.Element(f"{{{ns}}}ParameterSet", attrib={"name": "Waypoints"})
    params = ET.SubElement(root, f"{{{ns}}}Parameters")

    def add_param(name: str, type_tag: str, value: str) -> None:
        param_elem = ET.SubElement(params, f"{{{ns}}}Parameter", attrib={"name": name})
        value_elem = ET.SubElement(param_elem, f"{{{ns}}}{type_tag}")
        value_elem.set("value", value)

    if local_points:
        first = local_points[0]
        add_param("Environment.initX_km", "Real", f"{float(first['x_km']):.3f}")
        add_param("Environment.initY_km", "Real", f"{float(first['y_km']):.3f}")
        add_param("Environment.initZ_km", "Real", f"{float(first.get('z_km', 0.0)):.3f}")

        for idx, point in enumerate(local_points[1:], start=1):
            add_param(f"{component}.waypointX_km[{idx}]", "Real", f"{float(point['x_km']):.3f}")
            add_param(f"{component}.waypointY_km[{idx}]", "Real", f"{float(point['y_km']):.3f}")
            add_param(f"{component}.waypointZ_km[{idx}]", "Real", f"{float(point.get('z_km', 0.0)):.3f}")

    add_param(f"{component}.waypointCount", "Integer", str(len(local_points)-1))

    tree = ET.ElementTree(root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(tree, space="  ", level=0)
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)
    return output_path


def prepare_ssp_with_parameters(
    ssp_path: Path, parameter_set: Path, scenario_stem: str, results_dir: Path
) -> Path:
    run_dir = results_dir / f"{scenario_stem}_run"
    unpack_dir = run_dir / "unpacked"
    if unpack_dir.exists():
        shutil.rmtree(unpack_dir)
    unpack_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ssp_path, "r") as archive:
        archive.extractall(unpack_dir)

    resources_dir = unpack_dir / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)
    dest_ssv = resources_dir / parameter_set.name
    shutil.copy(parameter_set, dest_ssv)

    ssd_path = unpack_dir / "SystemStructure.ssd"
    ssd_ns = "http://ssp-standard.org/SSP1/SystemStructureDescription"
    ssc_ns = "http://ssp-standard.org/SSP1/SystemStructureCommon"
    ET.register_namespace("ssd", ssd_ns)
    ET.register_namespace("ssc", ssc_ns)
    ns = {"ssd": ssd_ns}
    tree = ET.parse(ssd_path)
    root = tree.getroot()
    system = root.find(".//ssd:System", ns)
    if system is None:
        system = root
    bindings = system.find("ssd:ParameterBindings", ns)
    if bindings is None:
        bindings = ET.SubElement(system, f"{{{ssd_ns}}}ParameterBindings")
    # remove duplicate bindings for same source
    for existing in list(bindings):
        if existing.get("source") == f"resources/{dest_ssv.name}":
            bindings.remove(existing)
    ET.SubElement(bindings, f"{{{ssd_ns}}}ParameterBinding", attrib={"source": f"resources/{dest_ssv.name}"})
    ET.indent(tree, space="  ")
    tree.write(ssd_path, encoding="UTF-8", xml_declaration=True)

    prepared_ssp = run_dir / f"{scenario_stem}.ssp"
    if prepared_ssp.exists():
        prepared_ssp.unlink()
    with zipfile.ZipFile(prepared_ssp, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in unpack_dir.rglob("*"):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(unpack_dir))
    return prepared_ssp


@dataclass
class RequirementEvaluation:
    identifier: str
    passed: bool
    evidence: str


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
    metrics: Dict[str, float] = field(default_factory=dict)
    requirement_evaluations: List[RequirementEvaluation] = field(default_factory=list)
    scenario_string: str = ""
    plot_path: Optional[Path] = None
    parameter_set_path: Optional[Path] = None
    prepared_ssp_path: Optional[Path] = None


def summarize_result_file(
    result_file: Path, scenario_points: Optional[List[Dict[str, float]]] = None
) -> Dict[str, float]:
    rows = _read_result_rows(result_file)
    time_series = _numeric_series(rows, "time")

    mach_series = _numeric_series(
        rows, "StructuralLoadsAndPerformanceMonitor.performanceStatus.mach_estimate"
    ) or _numeric_series(rows, "AirDataAndInertialSuite.airDataOut.mach_number")
    g_series = _numeric_series(
        rows, "StructuralLoadsAndPerformanceMonitor.performanceStatus.load_factor_g"
    )
    structural_margin = _numeric_series(
        rows,
        "StructuralLoadsAndPerformanceMonitor.performanceStatus.structural_margin_norm",
    )
    fuel_remaining = _numeric_series(
        rows, "TurbofanPropulsion.fuelStatus.fuel_remaining_kg"
    )
    fuel_level_norm = _numeric_series(
        rows, "TurbofanPropulsion.fuelStatus.fuel_level_norm"
    )
    fuel_starved = _numeric_series(rows, "TurbofanPropulsion.fuelStatus.fuel_starved")
    stores_masks = _numeric_series(
        rows, "StoresManagementSystem.storesTelemetry.store_present_mask", cast=int
    )
    autopilot_limits = _numeric_series(
        rows, "StructuralLoadsAndPerformanceMonitor.performanceStatus.autopilot_limit_code", cast=int
    ) or _numeric_series(
        rows, "AutopilotModule.performanceStatus.autopilot_limit_code", cast=int
    )
    energy_state = _numeric_series(
        rows, "AutopilotModule.feedbackBus.energy_state_norm"
    )
    thrust_kn = _numeric_series(rows, "TurbofanPropulsion.thrustOut.thrust_kn")
    mass_flow = _numeric_series(rows, "TurbofanPropulsion.thrustOut.mass_flow_kgps") or _numeric_series(
        rows, "TurbofanPropulsion.fuelFlow.mass_flow_kgps"
    )
    control_surface_excursions = [
        _span(_numeric_series(rows, "AdaptiveWingSystem.controlSurfaces.elevator_deg")),
        _span(_numeric_series(rows, "AdaptiveWingSystem.controlSurfaces.flaperon_deg")),
        _span(_numeric_series(rows, "FlyByWireController.commandBus.elevator_deg")),
    ]

    stores_available = 0
    if stores_masks:
        stores_available = max(int(mask).bit_count() for mask in stores_masks)

    fuel_initial_candidates = [v for v in fuel_remaining if v > 0]
    fuel_initial = (
        fuel_initial_candidates[0]
        if fuel_initial_candidates
        else (fuel_remaining[0] if fuel_remaining else 0.0)
    )
    fuel_final_candidates = [v for v in reversed(fuel_remaining) if v >= 0]
    fuel_final = fuel_final_candidates[0] if fuel_final_candidates else 0.0

    metrics = {
        "duration_s": time_series[-1] if time_series else 0.0,
        "max_mach": max(mach_series) if mach_series else 0.0,
        "max_load_factor_g": max(g_series) if g_series else 0.0,
        "min_structural_margin": min(structural_margin) if structural_margin else 1.0,
        "fuel_initial_kg": fuel_initial,
        "fuel_final_kg": fuel_final,
        "fuel_used_kg": max(fuel_initial - fuel_final, 0.0),
        "fuel_level_norm_min": min(fuel_level_norm) if fuel_level_norm else 0.0,
        "fuel_starved_events": len([v for v in fuel_starved if v > 0.5]),
        "stores_available": stores_available,
        "autopilot_limit_max": max(autopilot_limits) if autopilot_limits else 0,
        "energy_state_min": min(energy_state) if energy_state else 0.0,
        "thrust_kn_max": max(thrust_kn) if thrust_kn else 0.0,
        "mass_flow_kgps_max": max(mass_flow) if mass_flow else 0.0,
        "control_surface_excursion_deg": max(control_surface_excursions) if control_surface_excursions else 0.0,
    }
    track_points = extract_track_points(rows)
    metrics.update(
        waypoint_tracking_metrics(scenario_points or [], track_points)
    )
    return metrics


def evaluate_requirements(
    metrics: Dict[str, float], fuel_capacity_kg: float
) -> List[RequirementEvaluation]:
    reserve = fuel_capacity_kg * RESERVE_FRACTION
    evaluations = [
        RequirementEvaluation(
            identifier="REQ_Performance",
            passed=metrics.get("max_mach", 0.0) >= 2.0
            and metrics.get("max_load_factor_g", 0.0) >= 9.0,
            evidence=f"mach={metrics.get('max_mach', 0.0):.2f}, g-load={metrics.get('max_load_factor_g', 0.0):.2f}",
        ),
        RequirementEvaluation(
            identifier="REQ_Fuel",
            passed=metrics.get("fuel_final_kg", 0.0) >= reserve
            and metrics.get("fuel_starved_events", 0.0) == 0,
            evidence=f"final fuel={metrics.get('fuel_final_kg', 0.0):.1f} kg, reserve={reserve:.1f} kg",
        ),
        RequirementEvaluation(
            identifier="REQ_Control",
            passed=metrics.get("autopilot_limit_max", 1) == 0
            and metrics.get("control_surface_excursion_deg", 0.0) > 0.0,
            evidence=f"autopilot_limit={metrics.get('autopilot_limit_max', 1)}, control_excursion={metrics.get('control_surface_excursion_deg', 0.0):.2f} deg",
        ),
        RequirementEvaluation(
            identifier="REQ_Mission",
            passed=metrics.get("stores_available", 0) >= 9,
            evidence=f"stores_available={metrics.get('stores_available', 0)}",
        ),
        RequirementEvaluation(
            identifier="REQ_Propulsion",
            passed=metrics.get("thrust_kn_max", 0.0) > 0.0
            and metrics.get("mass_flow_kgps_max", 0.0) > 0.0,
            evidence=f"thrust={metrics.get('thrust_kn_max', 0.0):.1f} kN, mass_flow={metrics.get('mass_flow_kgps_max', 0.0):.2f} kg/s",
        ),
    ]
    return evaluations


# toggle log_fmu for more extensive logs
def run_with_simulator(ssp_path: Path, result_file: Path, stop_time: float, log_fmu = False) -> None:

    log_fmu = "true" if log_fmu else "false"

    config = f"""
{{
    "simulation" :
    {{
        "ssp": "{ssp_path.as_posix()}",
        "ssd": "SystemStructure.ssd",
        "start_time":0.0,
        "stop_time":{stop_time},
        "timestep": 1.0,
        "tolerance": 1e-4,

        "executor": 
        {{
            "method":"jacobi",
            
            "thread_pool_workers": 5,
            "forward_derivatives": true,

            "jacobi":
            {{
                "parallel": true,
                "method" : 1
            }},
            "seidel":
            {{
                "parallel": false
            }}
            
        }},

        "recording":
        {{
            "enable": true,
            "wait_for": true,
            "interval": 0.25,
            "result_file": "{result_file.as_posix()}"
        }},

        "log":
        {{
            "file": "./build/results/sim.log",
            "fmu": {log_fmu}
        }}
    }}
}}
"""
    temp_config = result_file.parent / "config.json"
    with open(temp_config, "w") as f:
        f.write(config)

    sim = pyssp4sim.Simulator(temp_config.as_posix())
    sim.init()
    sim.simulate()


def simulate_scenario(
    scenario_path: Path,
    ssp_path: Optional[Path] = None,
    results_dir: Path = DEFAULT_RESULTS,
    reuse_results: bool = True,
    stop_time: Optional[float] = None,
    plot: bool = False,
) -> ScenarioResult:
    scenario = load_json(scenario_path)
    if "points" not in scenario:
        raise ValueError("Scenario file must contain a 'points' list.")
    validate_scenario_points(scenario["points"])
    local_points = project_waypoints_to_local_km(scenario["points"])

    scenario_string = scenario_to_string(local_points)
    overrides = scenario.get("simulation_overrides", {})
    cruise_speed = float(overrides.get("cruise_speed_mps", 250.0))
    total_distance = scenario.get("total_distance_km") or local_path_distance_km(local_points) or haversine_distance_km(
        scenario["points"]
    )

    results_dir.mkdir(parents=True, exist_ok=True)
    result_file = results_dir / f"{scenario_path.stem}_results.csv"
    waypoints_file = results_dir / f"{scenario_path.stem}_waypoints.txt"
    waypoints_file.write_text(scenario_string)
    parameter_set_path = results_dir / f"{scenario_path.stem}_waypoints.ssv"
    emit_waypoint_parameter_set(local_points, parameter_set_path)
    prepared_ssp = prepare_ssp_with_parameters(ssp_path or DEFAULT_SSP, parameter_set_path, scenario_path.stem, results_dir)

    if stop_time is None:
        stop_time = max(estimate_duration(total_distance, cruise_speed) * 1.1, 120.0)

    if not reuse_results or not result_file.exists():
        if not prepared_ssp.exists():
            raise FileNotFoundError(f"Prepared SSP file not found: {prepared_ssp}")
        run_with_simulator(prepared_ssp, result_file, stop_time)

    metrics = summarize_result_file(result_file, scenario_points=local_points)
    metrics["total_distance_km"] = total_distance
    metrics["stop_time_s"] = stop_time

    fuel_capacity = float(
        overrides.get("fuel_capacity_kg", metrics.get("fuel_initial_kg", DEFAULT_FUEL_CAPACITY))
    )
    fuel_burn_rate = float(
        overrides.get(
            "fuel_burn_rate_kgps",
            metrics["fuel_used_kg"] / metrics["duration_s"] if metrics.get("duration_s") else 0.0,
        )
        or 0.0
    )
    estimated_duration = metrics.get("duration_s") or estimate_duration(
        total_distance, cruise_speed
    )
    fuel_required = metrics.get("fuel_used_kg") or estimated_duration * fuel_burn_rate

    reserve = fuel_capacity * RESERVE_FRACTION
    fuel_final = metrics.get("fuel_final_kg", fuel_capacity - fuel_required)
    fuel_exhausted = fuel_final <= 0 or fuel_final < reserve
    meets_range_requirement = fuel_required <= max(fuel_capacity - reserve, 0.0) and not fuel_exhausted

    requirement_evaluations = evaluate_requirements(metrics, fuel_capacity)
    plot_path = None

    summary = {
        "scenario": scenario.get("name", scenario_path.stem),
        "distance_km": total_distance,
        "duration_s": estimated_duration,
        "fuel_capacity_kg": fuel_capacity,
        "fuel_required_kg": fuel_required,
        "scenario_string": scenario_string,
        "requirements": [
            {"id": eval_.identifier, "passed": eval_.passed, "evidence": eval_.evidence}
            for eval_ in requirement_evaluations
        ],
        "metrics": {
            key: metrics[key]
            for key in [
                "max_mach",
                "max_load_factor_g",
                "fuel_initial_kg",
                "fuel_final_kg",
                "fuel_used_kg",
                "stores_available",
                "autopilot_limit_max",
                "thrust_kn_max",
                "mass_flow_kgps_max",
                "control_surface_excursion_deg",
                "waypoint_miss_max_km",
                "waypoint_miss_avg_km",
                "waypoint_hits",
                "waypoint_total",
                "waypoint_within_threshold_fraction",
                "waypoints_followed",
            ]
            if key in metrics
        },
    }

    if plot:
        requested_plot = results_dir / f"{scenario_path.stem}_path.png"
        plot_path = plot_flight_path(result_file, local_points, requested_plot)
        if plot_path:
            summary["plot_path"] = str(plot_path)

    summary_path = results_dir / f"{scenario_path.stem}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))

    return ScenarioResult(
        scenario_path=scenario_path,
        total_distance_km=total_distance,
        estimated_duration_s=estimated_duration,
        fuel_capacity_kg=fuel_capacity,
        fuel_burn_rate_kgps=fuel_burn_rate,
        fuel_required_kg=fuel_required,
        fuel_exhausted=fuel_exhausted,
        meets_range_requirement=meets_range_requirement,
        used_oms=result_file.exists(),
        result_file=result_file,
        metrics=metrics,
        requirement_evaluations=requirement_evaluations,
        scenario_string=scenario_string,
        plot_path=plot_path,
        parameter_set_path=parameter_set_path,
        prepared_ssp_path=prepared_ssp,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario", type=Path, required=True, help="Path to scenario JSON file."
    )
    parser.add_argument(
        "--ssp", type=Path, default=DEFAULT_SSP, help="Path to the SSP archive."
    )
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument(
        "--reuse-results",
        action="store_true",
        help="Skip OMSimulator run when a result CSV already exists for the scenario.",
    )
    parser.add_argument(
        "--stop-time",
        type=float,
        default=None,
        help="Override OMSimulator stop time in seconds.",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate a flight-path plot comparing simulated track to waypoints.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = simulate_scenario(
        scenario_path=args.scenario,
        ssp_path=args.ssp,
        results_dir=args.results_dir,
        reuse_results=args.reuse_results,
        stop_time=args.stop_time,
        plot=args.plot,
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
                "scenario_string": result.scenario_string,
                "parameter_set": str(result.parameter_set_path) if result.parameter_set_path else None,
                "plot_path": str(result.plot_path) if result.plot_path else None,
                "requirements": [
                    {"id": eval_.identifier, "passed": eval_.passed}
                    for eval_ in result.requirement_evaluations
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
