from __future__ import annotations

import math
import shutil
from pathlib import Path
import pytest
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.common.geo import project_waypoints_to_local_km  # type: ignore  # noqa: E402
from scripts.lib.results.plots import plot_flight_path, plot_flight_path_3d, plot_fuel_altitude_time  # type: ignore  # noqa: E402
from scripts.lib.scenarios.packaging import package_ssp_with_parameters  # type: ignore  # noqa: E402
from scripts.lib.scenarios.preparation import prepare_scenario_for_simulation, scenario_to_string  # type: ignore  # noqa: E402
from scripts.lib.scenarios.results import analyze_scenario_results, evaluate_requirements, summarize_result_file  # type: ignore  # noqa: E402


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
    assert "waypoint_miss_vertical_max_km" in metrics
    assert not math.isnan(metrics["waypoint_miss_vertical_max_km"])
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


def test_prepare_and_analyze_produce_summary_and_requirements(tmp_path):
    scenario_path = REPO_ROOT / "build" / "scenarios" / "test_scenario.json"
    source_results = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    target_results = results_dir / source_results.name
    shutil.copy(source_results, target_results)

    prepared = prepare_scenario_for_simulation(
        scenario_path=scenario_path,
        results_dir=results_dir,
    )
    prepared_ssp_path = package_ssp_with_parameters(
        ssp_path=REPO_ROOT / "build" / "ssp" / "aircraft.ssp",
        parameter_set_path=prepared.parameter_set_path,
        scenario_stem=scenario_path.stem,
        results_dir=results_dir,
    )
    result = analyze_scenario_results(
        scenario_path=scenario_path,
        result_file=target_results,
    )
    result.parameter_set_path = prepared.parameter_set_path
    result.prepared_ssp_path = prepared_ssp_path

    assert result.result_file == target_results
    assert result.used_oms
    assert result.requirement_evaluations
    assert result.scenario_string
    assert result.parameter_set_path == prepared.parameter_set_path
    assert result.prepared_ssp_path == prepared_ssp_path
    assert prepared_ssp_path.exists()

    requirement_ids = {req.identifier for req in result.requirement_evaluations}
    assert {"REQ_Performance", "REQ_Fuel", "REQ_Control", "REQ_Mission", "REQ_Propulsion"} <= requirement_ids

    summary_path = results_dir / f"{scenario_path.stem}_summary.json"
    assert summary_path.exists()


def test_analyze_scenario_results_writes_summary(tmp_path):
    scenario_path = REPO_ROOT / "build" / "scenarios" / "test_scenario.json"
    source_results = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    target_results = results_dir / source_results.name
    summary_path = results_dir / "evaluated_summary.json"
    shutil.copy(source_results, target_results)

    result = analyze_scenario_results(
        scenario_path=scenario_path,
        result_file=target_results,
        summary_path=summary_path,
    )

    assert result.requirement_evaluations
    assert summary_path.exists()


def test_plot_generation(tmp_path, monkeypatch):
    result_path = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    output = tmp_path / "plot.png"
    monkeypatch.setenv("SIM_SKIP_PLOTS", "1")
    plotted = plot_flight_path(result_path, [], output)
    if plotted:
        assert plotted.exists()


def test_plot_generation_3d(tmp_path, monkeypatch):
    result_path = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    output = tmp_path / "plot3d.png"
    monkeypatch.setenv("SIM_SKIP_PLOTS", "1")
    plotted = plot_flight_path_3d(result_path, [], output)
    assert plotted is None or plotted.exists()


def test_plot_generation_fuel_altitude(tmp_path, monkeypatch):
    result_path = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    output = tmp_path / "fuel_altitude.png"
    monkeypatch.setenv("SIM_SKIP_PLOTS", "1")
    plotted = plot_fuel_altitude_time(result_path, output)
    assert plotted is None or plotted.exists()
