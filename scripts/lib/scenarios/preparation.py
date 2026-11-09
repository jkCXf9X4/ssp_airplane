"""Scenario preparation helpers for simulation runs."""

from __future__ import annotations

import json
import math
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from pyssp_standard import SSV

from scripts.lib.common.geo import (
    haversine_distance_km,
    local_path_distance_km,
    project_waypoints_to_local_km,
)
from scripts.lib.paths import (
    BUILD_DIR,
    GENERATED_ANALYSIS_DESCRIPTOR,
    GENERATED_SCENARIO_SSM,
    GENERATED_SCENARIO_SSV,
)

DEFAULT_SSP = BUILD_DIR / "ssp" / "aircraft.ssp"
DEFAULT_RESULTS = BUILD_DIR / "results"


@dataclass
class PreparedScenario:
    scenario: dict
    scenario_path: Path
    local_points: List[Dict[str, float]]
    scenario_string: str
    total_distance_km: float
    cruise_speed_mps: float
    result_file: Path
    waypoints_file: Path
    parameter_set_path: Path
    ssm_path: Path
    analysis_descriptor_path: Path


def estimate_duration(distance_km: float, cruise_speed_mps: float) -> float:
    return max(60.0, (distance_km * 1000.0) / max(1.0, cruise_speed_mps))


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


WAYPOINT_ARRAY_SIZE = 10  # AutopilotModule.mo fixed waypoint array size.
WAYPOINT_PROXIMITY_KM = 10.0  # AutopilotModule.mo default arrival radius.


def _pad_waypoint_hops(
    local_points: List[Dict[str, float]], targets: List[Dict[str, float]], proximity_km: float
) -> List[Dict[str, float]]:
    """Extend the target list to the FMU's fixed array size.

    Arrivals only retrigger once the aircraft leaves the arrival radius of the
    next waypoint, so the padding continues along the final leg with hops that
    exceed the proximity threshold.
    """
    last = targets[-1] if targets else local_points[0]
    if len(targets) > 1:
        previous = targets[-2]
    else:
        previous = {"x_km": last["x_km"] - 1.0, "y_km": last["y_km"]}
    dx = last["x_km"] - previous["x_km"]
    dy = last["y_km"] - previous["y_km"]
    norm = math.hypot(dx, dy) or 1.0
    hop_km = proximity_km + 2.0
    padded = list(targets)
    for step in range(1, WAYPOINT_ARRAY_SIZE - len(targets) + 1):
        distance = hop_km * step
        padded.append(
            {
                "x_km": last["x_km"] + dx / norm * distance,
                "y_km": last["y_km"] + dy / norm * distance,
                "z_km": last.get("z_km", 0.0),
            }
        )
    return padded


def emit_waypoint_parameter_set(
    local_points: List[Dict[str, float]],
    output_path: Path,
    *,
    baseline_path: Path = GENERATED_SCENARIO_SSV,
    enable_bridge_input: bool = False,
    waypoint_proximity_km: float | None = None,
    target_airspeed_mps: float | None = None,
) -> Path:
    """Clone the generated scenario parameter set and override the waypoints.

    The baseline ``GENERATED_SCENARIO_SSV`` carries the architecture's bare
    scenario member names (``waypointX_km[1..10]``, ``initX_km``,
    ``useBridgeInput``, ...) that the analysis SSM maps onto component
    parameters. This helper copies the baseline to ``output_path`` and
    overrides the members the scenario drives, so the result stays on the bare
    name scheme the SSM applies. Waypoint indices are one-based to match the
    SSM mapping targets and the FMU-declared array indices.
    """
    if not baseline_path.is_file():
        raise FileNotFoundError(
            f"Scenario baseline parameter set not found: {baseline_path}. "
            "Regenerate the analysis artifacts from the architecture first."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(baseline_path, output_path)

    def add_or_override(ssv: SSV, name: str, value: str, type_name: str) -> None:
        parameter = ssv.parameters_by_name().get(name)
        if parameter is not None:
            parameter.attributes["value"] = value
        else:
            ssv.add_parameter(name, value, type_name=type_name)

    with SSV(output_path, mode="a") as ssv:
        add_or_override(ssv, "useBridgeInput", "true" if enable_bridge_input else "false", "Boolean")

        if local_points:
            first = local_points[0]
            add_or_override(ssv, "initX_km", f"{float(first['x_km']):.3f}", "Real")
            add_or_override(ssv, "initY_km", f"{float(first['y_km']):.3f}", "Real")
            add_or_override(ssv, "initZ_km", f"{float(first.get('z_km', 0.0)):.3f}", "Real")

            targets = local_points[1:]
            if len(targets) > WAYPOINT_ARRAY_SIZE:
                raise ValueError(
                    f"Scenario has {len(targets)} waypoints but the autopilot array holds at most {WAYPOINT_ARRAY_SIZE}."
                )
            targets = _pad_waypoint_hops(local_points, targets, float(waypoint_proximity_km or WAYPOINT_PROXIMITY_KM))

            # One-based indices matching the analysis SSM targets, e.g.
            # source="waypointX_km[1]" -> target="autopilot_module.waypointX_km[1]".
            for idx, point in enumerate(targets, start=1):
                add_or_override(ssv, f"waypointX_km[{idx}]", f"{float(point['x_km']):.3f}", "Real")
                add_or_override(ssv, f"waypointY_km[{idx}]", f"{float(point['y_km']):.3f}", "Real")
                add_or_override(ssv, f"waypointZ_km[{idx}]", f"{float(point.get('z_km', 0.0)):.3f}", "Real")

        if waypoint_proximity_km is not None:
            add_or_override(ssv, "waypointProximity_km", f"{float(waypoint_proximity_km):.3f}", "Real")
        if target_airspeed_mps is not None:
            add_or_override(ssv, "targetAirspeed_mps", f"{float(target_airspeed_mps):.3f}", "Real")

    return output_path


def prepare_scenario_for_simulation(
    scenario_path: Path,
    results_dir: Path = DEFAULT_RESULTS,
    bridge_input: bool = False,
    *,
    baseline_path: Path | None = None,
) -> PreparedScenario:
    scenario = json.loads(scenario_path.read_text())
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
    emit_waypoint_parameter_set(
        local_points,
        parameter_set_path,
        baseline_path=baseline_path or GENERATED_SCENARIO_SSV,
        enable_bridge_input=bridge_input,
        waypoint_proximity_km=overrides.get("waypoint_proximity_km"),
        target_airspeed_mps=overrides.get("target_airspeed_mps"),
    )

    return PreparedScenario(
        scenario=scenario,
        scenario_path=scenario_path,
        local_points=local_points,
        scenario_string=scenario_string,
        total_distance_km=float(total_distance),
        cruise_speed_mps=cruise_speed,
        result_file=result_file,
        waypoints_file=waypoints_file,
        parameter_set_path=parameter_set_path,
        ssm_path=GENERATED_SCENARIO_SSM,
        analysis_descriptor_path=GENERATED_ANALYSIS_DESCRIPTOR,
    )
