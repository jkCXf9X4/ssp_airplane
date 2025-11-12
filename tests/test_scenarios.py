from __future__ import annotations

import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from generate_scenario import generate_scenario  # type: ignore  # noqa: E402
from simulate_scenario import simulate_scenario  # type: ignore  # noqa: E402


def write_scenario(tmp_path: Path, scenario: dict) -> Path:
    path = tmp_path / "scenario.json"
    path.write_text(json.dumps(scenario, indent=2))
    return path


def test_short_scenario_meets_range_and_fuel(tmp_path):
    random.seed(7)
    scenario = generate_scenario(
        num_points=4,
        min_distance_km=150.0,
        max_distance_km=200.0,
        min_altitude_m=200.0,
        max_altitude_m=5000.0,
    )
    scenario_path = write_scenario(tmp_path, scenario)
    result = simulate_scenario(
        scenario_path=scenario_path,
        use_oms=False,
        cruise_speed_mps=240.0,
        fuel_capacity_kg=2000.0,
        fuel_burn_rate_kgps=0.5,
    )
    assert result.total_distance_km >= 150
    assert result.meets_range_requirement
    assert not result.fuel_exhausted


def test_long_scenario_runs_out_of_fuel(tmp_path):
    random.seed(21)
    scenario = generate_scenario(
        num_points=8,
        min_distance_km=1800.0,
        max_distance_km=2200.0,
        min_altitude_m=500.0,
        max_altitude_m=8000.0,
    )
    scenario_path = write_scenario(tmp_path, scenario)
    result = simulate_scenario(
        scenario_path=scenario_path,
        use_oms=False,
        cruise_speed_mps=250.0,
        fuel_capacity_kg=1200.0,
        fuel_burn_rate_kgps=0.7,
    )
    assert result.total_distance_km >= 1800
    assert result.fuel_required_kg > result.fuel_capacity_kg
    assert result.fuel_exhausted
