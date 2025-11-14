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


def test_high_altitude_intercept_meets_performance_requirement():
    scenario, path = load_use_case("high_altitude_intercept")
    overrides = scenario["simulation_overrides"]
    result = simulate_scenario(
        scenario_path=path,
        use_oms=False,
        cruise_speed_mps=overrides["cruise_speed_mps"],
        fuel_capacity_kg=overrides["fuel_capacity_kg"],
        fuel_burn_rate_kgps=overrides["fuel_burn_rate_kgps"],
    )
    avg_speed_mps = result.total_distance_km * 1000 / result.estimated_duration_s
    mach = avg_speed_mps / 340.0
    assert mach >= 2.0, "Mach 2 dash capability must be preserved"
    assert result.meets_range_requirement
    assert not result.fuel_exhausted


def test_deep_strike_preserves_fuel_reserve():
    scenario, path = load_use_case("deep_strike_penetration")
    overrides = scenario["simulation_overrides"]
    reserve_fraction = 0.08
    result = simulate_scenario(
        scenario_path=path,
        use_oms=False,
        cruise_speed_mps=overrides["cruise_speed_mps"],
        fuel_capacity_kg=overrides["fuel_capacity_kg"],
        fuel_burn_rate_kgps=overrides["fuel_burn_rate_kgps"],
    )
    usable_fuel = overrides["fuel_capacity_kg"] * (1 - reserve_fraction)
    assert result.total_distance_km >= 3000
    assert result.fuel_required_kg <= usable_fuel
    assert not result.fuel_exhausted
    assert result.meets_range_requirement


def test_cas_mission_supports_full_stores_payload():
    scenario, path = load_use_case("cas_multi_store_support")
    overrides = scenario["simulation_overrides"]
    mission_profile = scenario["mission_profile"]
    result = simulate_scenario(
        scenario_path=path,
        use_oms=False,
        cruise_speed_mps=overrides["cruise_speed_mps"],
        fuel_capacity_kg=overrides["fuel_capacity_kg"],
        fuel_burn_rate_kgps=overrides["fuel_burn_rate_kgps"],
    )
    assert mission_profile["stations_used"] == 9
    assert mission_profile["stores_payload_kg"] <= 7700
    assert not result.fuel_exhausted
    assert result.meets_range_requirement
