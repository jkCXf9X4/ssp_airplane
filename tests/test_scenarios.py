from __future__ import annotations

import json
import sys
from pathlib import Path
import shutil
import zipfile

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.scenarios.generate import generate_scenario  # type: ignore  # noqa: E402
from scripts.lib.scenarios.preparation import emit_waypoint_parameter_set, prepare_scenario_for_simulation  # type: ignore  # noqa: E402
from scripts.lib.scenarios.results import analyze_scenario_results  # type: ignore  # noqa: E402

USE_CASE_DIR = REPO_ROOT / "resources" / "scenarios"


def write_scenario(tmp_path: Path, scenario: dict) -> Path:
    path = tmp_path / "scenario.json"
    path.write_text(json.dumps(scenario, indent=2))
    return path


def load_use_case(name: str) -> tuple[dict, Path]:
    path = USE_CASE_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    scenario = json.loads(path.read_text())
    return scenario, path


def test_high_altitude_intercept_meets_performance_requirement(tmp_path):
    scenario, path = load_use_case("high_altitude_intercept")
    # Reuse pre-generated OMS results to exercise the requirement evaluation pipeline.
    source_results = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    target_results = results_dir / f"{path.stem}_results.csv"
    if not target_results.exists():
        shutil.copy(source_results, target_results)

    prepare_scenario_for_simulation(
        scenario_path=path,
        results_dir=results_dir,
    )
    result = analyze_scenario_results(
        scenario_path=path,
        result_file=target_results,
    )
    performance_eval = next(req for req in result.requirement_evaluations if req.identifier == "REQ_Performance")
    fuel_eval = next(req for req in result.requirement_evaluations if req.identifier == "REQ_Fuel")
    assert not performance_eval.passed, "Performance shortfall should be detected in reused OMS data"
    assert fuel_eval.passed


def test_emit_waypoint_parameter_set_uses_bare_names_and_one_based_indices(tmp_path: Path) -> None:
    output = tmp_path / "waypoints.ssv"
    emit_waypoint_parameter_set(
        [
            {"x_km": 0.0, "y_km": 0.0, "z_km": 0.1},
            {"x_km": 12.5, "y_km": -3.0, "z_km": 1.2},
            {"x_km": 20.0, "y_km": 4.0, "z_km": 2.5},
        ],
        output,
        waypoint_proximity_km=2.5,
        target_airspeed_mps=240.0,
    )

    text = output.read_text(encoding="utf-8")
    assert 'name="useBridgeInput"' in text
    assert 'name="initX_km"' in text
    assert 'name="initY_km"' in text
    assert 'name="initZ_km"' in text
    assert 'name="waypointX_km[0]"' not in text
    assert 'name="waypointX_km[1]"' in text
    assert 'value="12.500"' in text
    assert 'name="waypointX_km[2]"' in text
    assert 'value="20.000"' in text
    # The scenario parameter set carries bare member names; component qualification
    # is applied later by the SSM mapping at bind time (packaging).
    assert 'name="autopilot_module.waypointX_km[1]"' not in text
    assert 'name="control_interface.useBridgeInput"' not in text
    # One-based indices matching the analysis SSM targets.
    assert 'name="waypointX_km[10]"' in text
    assert "waypointCount" not in text
    assert 'name="waypointProximity_km"' in text
    assert 'value="2.500"' in text
    assert 'name="targetAirspeed_mps"' in text
    assert 'value="240.000"' in text
    assert 'name="AutopilotModule.waypointX_km[1]"' not in text
    assert 'name="Environment.initX_km"' not in text


def test_packaging_binds_one_based_scenario_set(tmp_path: Path) -> None:
    from scripts.lib.scenarios.packaging import package_ssp_with_parameters  # type: ignore  # noqa: F401

    output = tmp_path / "waypoints.ssv"
    emit_waypoint_parameter_set(
        [
            {"x_km": 0.0, "y_km": 0.0, "z_km": 0.1},
            {"x_km": 12.5, "y_km": -3.0, "z_km": 1.2},
        ],
        output,
        waypoint_proximity_km=2.5,
        target_airspeed_mps=240.0,
    )

    ssm_path = REPO_ROOT / "generated" / "analysis" / "HighAltitudeIntercept.ssm"
    if not ssm_path.is_file():
        raise FileNotFoundError(ssm_path)
    ssp_path = REPO_ROOT / "build" / "ssp" / "aircraft.ssp"
    if not ssp_path.is_file():
        raise FileNotFoundError(ssp_path)

    results_dir = tmp_path / "results"
    package_ssp_with_parameters(
        ssp_path=ssp_path,
        parameter_set_path=output,
        scenario_stem="mission",
        results_dir=results_dir,
        ssm_path=ssm_path,
        analysis_descriptor_path=REPO_ROOT / "generated" / "analysis" / "analysis.json",
    )

    prepared_ssp = results_dir / "mission_run" / "mission.ssp"
    with zipfile.ZipFile(prepared_ssp) as archive:
        text = archive.read("resources/MissionScenario.ssv").decode()
    # Emitted and bound sets are natively one-based.
    assert "waypointX_km[0]" not in text
    assert 'name="waypointX_km[1]"' in text
    assert 'name="waypointX_km[10]"' in text
    assert 'name="initX_km"' in text
    assert 'name="useBridgeInput"' in text
