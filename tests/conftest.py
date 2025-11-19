from __future__ import annotations

from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_SCENARIO = REPO_ROOT / "resources" / "scenarios" / "test_scenario.json"
SAMPLE_RESULTS = REPO_ROOT / "resources" / "references" / "test_scenario_results.csv"
BUILD_SCENARIO = REPO_ROOT / "build" / "scenarios" / "test_scenario.json"
BUILD_RESULTS = REPO_ROOT / "build" / "results" / "test_scenario_results.csv"


def pytest_configure(config):  # noqa: D401
    """Ensure reusable scenario/results artifacts exist under build/ for test reuse."""
    ensure_test_artifacts()


def ensure_test_artifacts() -> None:
    """Copy canned scenario/results into build/ if they do not exist."""
    mappings = (
        (SAMPLE_SCENARIO, BUILD_SCENARIO),
        (SAMPLE_RESULTS, BUILD_RESULTS),
    )
    for src, dst in mappings:
        if not src.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy(src, dst)
