#!/usr/bin/env python3
"""CLI for scenario waypoint preparation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.lib.scenarios.preparation import DEFAULT_RESULTS, prepare_scenario_for_simulation


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate waypoint artifacts for a scenario.")
    parser.add_argument("--scenario", type=Path, required=True, help="Path to scenario JSON file.")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS, help="Directory for generated artifacts.")
    parser.add_argument(
        "--bridge-input",
        action="store_true",
        help="Enable interactive bridge/manual input with scripted fallback when no live command stream is present.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    prepared = prepare_scenario_for_simulation(
        scenario_path=args.scenario,
        results_dir=args.results_dir,
        bridge_input=args.bridge_input,
    )
    print(
        json.dumps(
            {
                "scenario": str(prepared.scenario_path),
                "scenario_name": prepared.scenario.get("name", prepared.scenario_path.stem),
                "total_distance_km": prepared.total_distance_km,
                "cruise_speed_mps": prepared.cruise_speed_mps,
                "result_file": str(prepared.result_file),
                "waypoints_file": str(prepared.waypoints_file),
                "parameter_set": str(prepared.parameter_set_path),
                "scenario_string": prepared.scenario_string,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
