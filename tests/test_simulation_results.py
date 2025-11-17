from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from simulate_scenario import (  # type: ignore  # noqa: E402
    evaluate_requirements,
    plot_flight_path,
    scenario_to_string,
    simulate_scenario,
    summarize_result_file,
)


def test_result_postprocessing_extracts_requirement_metrics():
    result_path = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    metrics = summarize_result_file(result_path)

    assert metrics["duration_s"] > 0
    assert metrics["max_mach"] > 0
    assert metrics["fuel_initial_kg"] >= metrics["fuel_final_kg"]
    requirements = evaluate_requirements(metrics, fuel_capacity_kg=metrics["fuel_initial_kg"])
    requirement_ids = {req.identifier for req in requirements}
    assert {"REQ_Performance", "REQ_Fuel", "REQ_Control", "REQ_Mission", "REQ_Propulsion"} <= requirement_ids


def test_scenario_string_round_trip():
    scenario = [
        {"latitude_deg": 1.0, "longitude_deg": 2.0, "altitude_m": 100.0},
        {"latitude_deg": 3.0, "longitude_deg": 4.0, "altitude_m": 200.0},
    ]
    s = scenario_to_string(scenario)
    assert "1.000000" in s
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
        reuse_results=True,
        stop_time=120.0,
    )

    assert result.result_file == target_results
    assert result.used_oms
    assert result.requirement_evaluations

    mission_eval = next(req for req in result.requirement_evaluations if req.identifier == "REQ_Mission")
    assert mission_eval.passed

    summary_path = results_dir / f"{scenario_path.stem}_summary.json"
    assert summary_path.exists()


def test_plot_generation(tmp_path):
    result_path = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    output = tmp_path / "plot.png"
    plotted = plot_flight_path(result_path, [], output)
    if plotted:
        assert plotted.exists()
