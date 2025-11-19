from __future__ import annotations

import math
import os
import shutil
from pathlib import Path
import pytest
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.workflows.simulate_scenario import (  # type: ignore  # noqa: E402
    evaluate_requirements,
    plot_flight_path,
    project_waypoints_to_local_km,
    scenario_to_string,
    simulate_scenario,
    summarize_result_file,
)


def test_result_postprocessing_extracts_requirement_metrics():
    result_path = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    scenario = (REPO_ROOT / "build" / "scenarios" / "test_scenario.json").read_text()
    import json
    scenario_points = json.loads(scenario)["points"]
    local_points = project_waypoints_to_local_km(scenario_points)
    metrics = summarize_result_file(result_path, scenario_points=local_points)

    assert metrics["duration_s"] > 0
    assert metrics["max_mach"] > 0
    assert metrics["fuel_initial_kg"] >= metrics["fuel_final_kg"]
    assert "waypoint_miss_max_km" in metrics
    assert not math.isnan(metrics["waypoint_miss_max_km"])
    assert "waypoints_followed" in metrics
    requirements = evaluate_requirements(metrics, fuel_capacity_kg=metrics["fuel_initial_kg"])
    requirement_ids = {req.identifier for req in requirements}
    assert {"REQ_Performance", "REQ_Fuel", "REQ_Control", "REQ_Mission", "REQ_Propulsion"} <= requirement_ids


def test_scenario_string_round_trip():
    local_points = [
        {"x_km": 0.0, "y_km": 0.0, "z_km": 0.1},
        {"x_km": 5.0, "y_km": 10.0, "z_km": 0.2},
    ]
    s = scenario_to_string(local_points)
    assert "5.000" in s
    assert s.count(",") == len(s.split(",")) - 1


def test_simulation_reuse_produces_summary_and_requirements(tmp_path):
    scenario_path = REPO_ROOT / "build" / "scenarios" / "test_scenario.json"
    source_results = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    target_results = results_dir / source_results.name
    shutil.copy(source_results, target_results)

    result = simulate_scenario(
        scenario_path=scenario_path,
        ssp_path=REPO_ROOT / "build" / "ssp" / "aircraft.ssp",
        results_dir=results_dir,
        reuse_results=False,
        stop_time=120.0,
    )

    assert result.result_file == target_results
    assert result.used_oms
    assert result.requirement_evaluations
    assert result.scenario_string

    mission_eval = next(req for req in result.requirement_evaluations if req.identifier == "REQ_Mission")
    assert mission_eval.passed

    summary_path = results_dir / f"{scenario_path.stem}_summary.json"
    assert summary_path.exists()


def test_plot_generation(tmp_path):
    result_path = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    output = tmp_path / "plot.png"
    os.environ["SIM_SKIP_PLOTS"] = "1"
    plotted = plot_flight_path(result_path, [], output)
    if plotted:
        assert plotted.exists()
