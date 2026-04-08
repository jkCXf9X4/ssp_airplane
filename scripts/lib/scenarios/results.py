"""Scenario result analysis and requirement evaluation."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from scripts.lib.common.csv import numeric_series, read_result_rows, series_from_candidates
from scripts.lib.common.geo import haversine_distance_km, local_path_distance_km, project_waypoints_to_local_km
from scripts.lib.results.track import extract_track_points
from scripts.lib.scenarios.preparation import scenario_to_string, validate_scenario_points

DEFAULT_FUEL_CAPACITY = 3100.0
RESERVE_FRACTION = 0.08
WAYPOINT_HIT_THRESHOLD_KM = 10.0
WAYPOINT_ALTITUDE_HIT_THRESHOLD_KM = 0.5


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
    parameter_set_path: Optional[Path] = None
    prepared_ssp_path: Optional[Path] = None


def _scenario_distance_km(scenario: dict, local_points: List[Dict[str, float]]) -> float:
    return float(
        scenario.get("total_distance_km")
        or local_path_distance_km(local_points)
        or haversine_distance_km(scenario["points"])
    )


def scenario_result_payload(result: ScenarioResult) -> dict[str, object]:
    return {
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
        "requirements": [
            {"id": evaluation.identifier, "passed": evaluation.passed}
            for evaluation in result.requirement_evaluations
        ],
    }


def analyze_scenario_results(
    scenario_path: Path,
    result_file: Path,
    summary_path: Optional[Path] = None,
) -> ScenarioResult:
    scenario = json.loads(scenario_path.read_text())
    if "points" not in scenario:
        raise ValueError("Scenario file must contain a 'points' list.")

    validate_scenario_points(scenario["points"])
    local_points = project_waypoints_to_local_km(scenario["points"])
    scenario_string = scenario_to_string(local_points)
    total_distance_km = _scenario_distance_km(scenario, local_points)
    metrics = summarize_result_file(result_file, scenario_points=local_points)
    metrics["total_distance_km"] = total_distance_km
    metrics["stop_time_s"] = metrics.get("duration_s", 0.0)

    overrides = scenario.get("simulation_overrides", {})
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
    estimated_duration = float(metrics.get("duration_s", 0.0))
    fuel_required = metrics.get("fuel_used_kg") or estimated_duration * fuel_burn_rate

    reserve = fuel_capacity * RESERVE_FRACTION
    fuel_final = metrics.get("fuel_final_kg", fuel_capacity - fuel_required)
    fuel_exhausted = fuel_final <= 0 or fuel_final < reserve
    meets_range_requirement = fuel_required <= max(fuel_capacity - reserve, 0.0) and not fuel_exhausted

    requirement_evaluations = evaluate_requirements(metrics, fuel_capacity)
    result = ScenarioResult(
        scenario_path=scenario_path,
        total_distance_km=total_distance_km,
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
    )

    resolved_summary_path = summary_path or (result_file.parent / f"{scenario_path.stem}_summary.json")
    resolved_summary_path.write_text(
        json.dumps(
            {
                "scenario": scenario.get("name", scenario_path.stem),
                "distance_km": total_distance_km,
                "duration_s": estimated_duration,
                "fuel_capacity_kg": fuel_capacity,
                "fuel_required_kg": fuel_required,
                "scenario_string": scenario_string,
                "requirements": [
                    {"id": evaluation.identifier, "passed": evaluation.passed, "evidence": evaluation.evidence}
                    for evaluation in requirement_evaluations
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
                        "waypoint_miss_vertical_max_km",
                        "waypoint_miss_vertical_avg_km",
                        "waypoint_hits",
                        "waypoint_total",
                        "waypoint_within_threshold_fraction",
                        "waypoints_followed",
                    ]
                    if key in metrics
                },
            },
            indent=2,
        )
    )
    return result


def waypoint_tracking_metrics(
    scenario_points: List[Dict[str, float]],
    track_points: List[Tuple[float, float, float]],
    threshold_km: float = WAYPOINT_HIT_THRESHOLD_KM,
    vertical_threshold_km: float = WAYPOINT_ALTITUDE_HIT_THRESHOLD_KM,
) -> Dict[str, float]:
    if not scenario_points or not track_points:
        return {
            "waypoint_miss_max_km": float("nan"),
            "waypoint_miss_avg_km": float("nan"),
            "waypoint_miss_vertical_max_km": float("nan"),
            "waypoint_miss_vertical_avg_km": float("nan"),
            "waypoint_hits": 0,
            "waypoint_total": len(scenario_points),
            "waypoint_within_threshold_fraction": 0.0,
        }

    misses: List[float] = []
    vertical_misses: List[float] = []
    hits = 0
    for wp in scenario_points:
        x = float(wp["x_km"])
        y = float(wp["y_km"])
        z = float(wp.get("z_km", 0.0))
        best_distance = float("inf")
        best_planar = float("inf")
        best_vertical = float("inf")
        for track_point in track_points:
            dx = x - track_point[0]
            dy = y - track_point[1]
            dz = z - track_point[2]
            planar = math.sqrt(dx * dx + dy * dy)
            vertical_sep = abs(dz)
            distance = math.sqrt(planar * planar + dz * dz)
            best_planar = min(best_planar, planar)
            best_vertical = min(best_vertical, vertical_sep)
            best_distance = min(best_distance, distance)
        misses.append(best_planar)
        vertical_misses.append(best_vertical)
        if best_distance <= threshold_km and best_vertical <= vertical_threshold_km:
            hits += 1

    total = len(scenario_points)
    return {
        "waypoint_miss_max_km": max(misses),
        "waypoint_miss_avg_km": sum(misses) / total if total else float("nan"),
        "waypoint_miss_vertical_max_km": max(vertical_misses),
        "waypoint_miss_vertical_avg_km": sum(vertical_misses) / total if total else float("nan"),
        "waypoint_hits": hits,
        "waypoint_total": total,
        "waypoint_within_threshold_fraction": hits / total if total else 0.0,
        "waypoints_followed": 1.0 if total and hits == total else 0.0,
    }


def summarize_result_file(
    result_file: Path,
    scenario_points: Optional[List[Dict[str, float]]] = None,
) -> Dict[str, float]:
    rows = read_result_rows(result_file)
    time_series = numeric_series(rows, "time")

    mach_series = series_from_candidates(
        rows,
        [
            "structural_loads_and_performance_monitor.performanceStatus.mach_estimate",
            "StructuralLoadsAndPerformanceMonitor.performanceStatus.mach_estimate",
            "air_data_and_inertial_suite.airDataOut.mach_number",
            "AirDataAndInertialSuite.airDataOut.mach_number",
        ],
    )
    if not mach_series:
        airspeed_series = series_from_candidates(
            rows,
            [
                "environment.flight_status.airspeed_mps",
                "Environment.flight_speed.airspeed_mps",
                "autopilot_module.feedbackBus.airspeed_mps",
                "AutopilotModule.feedbackBus.airspeed_mps",
                "flightgear_bridge.flightStatus.airspeed_mps",
                "FlightGearBridge.flightStatus.airspeed_mps",
            ],
        )
        mach_series = [airspeed / 340.29 for airspeed in airspeed_series]
    g_series = series_from_candidates(
        rows,
        [
            "structural_loads_and_performance_monitor.performanceStatus.load_factor_g",
            "StructuralLoadsAndPerformanceMonitor.performanceStatus.load_factor_g",
        ],
    )
    structural_margin = series_from_candidates(
        rows,
        [
            "structural_loads_and_performance_monitor.performanceStatus.structural_margin_norm",
            "StructuralLoadsAndPerformanceMonitor.performanceStatus.structural_margin_norm",
        ],
    )
    fuel_remaining = series_from_candidates(
        rows,
        [
            "turbofan_propulsion.fuelStatus.fuel_remaining_kg",
            "TurbofanPropulsion.fuelStatus.fuel_remaining_kg",
            "fuel_system.fuelState.fuel_remaining_kg",
            "FuelSystem.fuelState.fuel_remaining_kg",
            "mission_computer.fuelStatus.fuel_remaining_kg",
            "MissionComputer.fuelStatus.fuel_remaining_kg",
        ],
    )
    fuel_level_norm = series_from_candidates(
        rows,
        [
            "turbofan_propulsion.fuelStatus.fuel_level_norm",
            "TurbofanPropulsion.fuelStatus.fuel_level_norm",
            "fuel_system.fuelState.fuel_level_norm",
            "FuelSystem.fuelState.fuel_level_norm",
            "mission_computer.fuelStatus.fuel_level_norm",
            "MissionComputer.fuelStatus.fuel_level_norm",
        ],
    )
    fuel_starved = series_from_candidates(
        rows,
        [
            "turbofan_propulsion.fuelStatus.fuel_starved",
            "TurbofanPropulsion.fuelStatus.fuel_starved",
            "fuel_system.fuelState.fuel_starved",
            "FuelSystem.fuelState.fuel_starved",
            "mission_computer.fuelStatus.fuel_starved",
            "MissionComputer.fuelStatus.fuel_starved",
        ],
    )
    stores_masks = series_from_candidates(
        rows,
        [
            "stores_management_system.storesTelemetry.store_present_mask",
            "StoresManagementSystem.storesTelemetry.store_present_mask",
        ],
        cast=int,
    )
    hardpoint_count = series_from_candidates(
        rows,
        [
            "composite_airframe.hardpoint_count",
            "CompositeAirframe.hardpoint_count",
        ],
        cast=int,
    )
    autopilot_limits = series_from_candidates(
        rows,
        [
            "structural_loads_and_performance_monitor.performanceStatus.autopilot_limit_code",
            "StructuralLoadsAndPerformanceMonitor.performanceStatus.autopilot_limit_code",
            "autopilot_module.performanceStatus.autopilot_limit_code",
            "AutopilotModule.performanceStatus.autopilot_limit_code",
        ],
        cast=int,
    )
    energy_state = series_from_candidates(
        rows,
        [
            "autopilot_module.feedbackBus.energy_state_norm",
            "AutopilotModule.feedbackBus.energy_state_norm",
        ],
    )
    thrust_kn = series_from_candidates(
        rows,
        [
            "turbofan_propulsion.thrustOut.thrust_kn",
            "TurbofanPropulsion.thrustOut.thrust_kn",
        ],
    )
    mass_flow = series_from_candidates(
        rows,
        [
            "turbofan_propulsion.thrustOut.mass_flow_kgps",
            "TurbofanPropulsion.thrustOut.mass_flow_kgps",
            "turbofan_propulsion.fuelFlow.mass_flow_kgps",
            "TurbofanPropulsion.fuelFlow.mass_flow_kgps",
            "turbofan_propulsion.fuel_consumption.mass_flow_kgps",
            "TurbofanPropulsion.fuel_consumption.mass_flow_kgps",
            "fuel_system.fuel_consumption_rate.mass_flow_kgps",
            "FuelSystem.fuel_consumption_rate.mass_flow_kgps",
        ],
    )
    control_surface_excursions: List[float] = []
    for key in (
        "adaptive_wing_system.actuation_command.elevator_deg",
        "adaptive_wing_system.actuation_command.flaperon_deg",
        "adaptive_wing_system.actuation_command.left_aileron_deg",
        "adaptive_wing_system.actuation_command.right_aileron_deg",
        "adaptive_wing_system.actuation_command.rudder_deg",
        "environment.actuation_command.elevator_deg",
        "AdaptiveWingSystem.controlSurfaces.elevator_deg",
        "AdaptiveWingSystem.controlSurfaces.flaperon_deg",
        "FlyByWireController.commandBus.elevator_deg",
        "AdaptiveWingSystem.actuation_command.elevator_deg",
        "AdaptiveWingSystem.actuation_command.flaperon_deg",
        "AdaptiveWingSystem.actuation_command.left_aileron_deg",
        "AdaptiveWingSystem.actuation_command.right_aileron_deg",
        "AdaptiveWingSystem.actuation_command.rudder_deg",
        "Environment.actuation_command.elevator_deg",
    ):
        series = numeric_series(rows, key)
        control_surface_excursions.append(max(series) - min(series) if series else 0.0)

    stores_available = 0
    if stores_masks:
        stores_available = max(int(mask).bit_count() for mask in stores_masks)
    elif hardpoint_count:
        stores_available = max(hardpoint_count)

    fuel_initial_candidates = [value for value in fuel_remaining if value > 0]
    fuel_initial = (
        fuel_initial_candidates[0]
        if fuel_initial_candidates
        else (fuel_remaining[0] if fuel_remaining else 0.0)
    )
    fuel_final_candidates = [value for value in reversed(fuel_remaining) if value >= 0]
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
        "fuel_starved_events": len([value for value in fuel_starved if value > 0.5]),
        "stores_available": stores_available,
        "autopilot_limit_max": max(autopilot_limits) if autopilot_limits else 0,
        "energy_state_min": min(energy_state) if energy_state else 0.0,
        "thrust_kn_max": max(thrust_kn) if thrust_kn else 0.0,
        "mass_flow_kgps_max": max(mass_flow) if mass_flow else 0.0,
        "control_surface_excursion_deg": max(control_surface_excursions) if control_surface_excursions else 0.0,
    }
    track_points = extract_track_points(rows)
    metrics.update(waypoint_tracking_metrics(scenario_points or [], track_points))
    return metrics


def evaluate_requirements(
    metrics: Dict[str, float],
    fuel_capacity_kg: float,
) -> List[RequirementEvaluation]:
    reserve = fuel_capacity_kg * RESERVE_FRACTION
    return [
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
