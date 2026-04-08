"""Scenario preparation helpers for simulation runs."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import xml.etree.ElementTree as ET

from scripts.lib.common.geo import (
    haversine_distance_km,
    local_path_distance_km,
    project_waypoints_to_local_km,
)
from scripts.lib.paths import BUILD_DIR

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


def emit_waypoint_parameter_set(
    local_points: List[Dict[str, float]],
    output_path: Path,
    component: str = "AutopilotModule",
    enable_bridge_input: bool = False,
) -> Path:
    ns = "http://ssp-standard.org/SSP1/ParameterValues"
    ET.register_namespace("ssv", ns)
    root = ET.Element(f"{{{ns}}}ParameterSet", attrib={"name": "Waypoints"})
    params = ET.SubElement(root, f"{{{ns}}}Parameters")

    def add_param(name: str, type_tag: str, value: str) -> None:
        param_elem = ET.SubElement(params, f"{{{ns}}}Parameter", attrib={"name": name})
        value_elem = ET.SubElement(param_elem, f"{{{ns}}}{type_tag}")
        value_elem.set("value", value)

    add_param("ControlInterface.useBridgeInput", "Boolean", "true" if enable_bridge_input else "false")

    if local_points:
        first = local_points[0]
        add_param("Environment.initX_km", "Real", f"{float(first['x_km']):.3f}")
        add_param("Environment.initY_km", "Real", f"{float(first['y_km']):.3f}")
        add_param("Environment.initZ_km", "Real", f"{float(first.get('z_km', 0.0)):.3f}")

        for idx, point in enumerate(local_points[1:], start=1):
            add_param(f"{component}.waypointX_km[{idx}]", "Real", f"{float(point['x_km']):.3f}")
            add_param(f"{component}.waypointY_km[{idx}]", "Real", f"{float(point['y_km']):.3f}")
            add_param(f"{component}.waypointZ_km[{idx}]", "Real", f"{float(point.get('z_km', 0.0)):.3f}")

    add_param(f"{component}.waypointCount", "Integer", str(len(local_points) - 1))

    tree = ET.ElementTree(root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(tree, space="  ", level=0)
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)
    return output_path


def prepare_scenario_for_simulation(
    scenario_path: Path,
    results_dir: Path = DEFAULT_RESULTS,
    bridge_input: bool = False,
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
    emit_waypoint_parameter_set(local_points, parameter_set_path, enable_bridge_input=bridge_input)

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
    )
