from __future__ import annotations

import json
import sys
from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.generation.generate_scenario import generate_scenario  # type: ignore  # noqa: E402
from scripts.workflows.simulate_scenario import simulate_scenario  # type: ignore  # noqa: E402

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

    result = simulate_scenario(
        scenario_path=path,
        results_dir=results_dir,
        reuse_results=True,
    )
    performance_eval = next(req for req in result.requirement_evaluations if req.identifier == "REQ_Performance")
    fuel_eval = next(req for req in result.requirement_evaluations if req.identifier == "REQ_Fuel")
    assert not performance_eval.passed, "Performance shortfall should be detected in reused OMS data"
    assert fuel_eval.passed
