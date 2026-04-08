#!/usr/bin/env python3
"""CLI for scenario simulation runs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.lib.scenarios.simulate import (
    DEFAULT_RESULTS,
    DEFAULT_SSP,
    scenario_result_summary,
    simulate_scenario,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or reuse a scenario simulation.")
    parser.add_argument("--scenario", type=Path, required=True, help="Path to scenario JSON file.")
    parser.add_argument("--ssp", type=Path, default=DEFAULT_SSP, help="Path to the SSP archive.")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument(
        "--reuse-results",
        action="store_true",
        help="Skip ssp4sim run when a result CSV already exists for the scenario.",
    )
    parser.add_argument(
        "--stop-time",
        type=float,
        default=None,
        help="Override ssp4sim stop time in seconds.",
    )
    parser.add_argument(
        "--realtime",
        action="store_true",
        help="Enable ssp4sim realtime pacing.",
    )
    parser.add_argument(
        "--config-path",
        type=Path,
        default=None,
        help="Optional path to write the simulator config JSON to before launching.",
    )
    parser.add_argument(
        "--bridge-input",
        action="store_true",
        help="Enable interactive bridge/manual input with scripted fallback when no live command stream is present.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = simulate_scenario(
        scenario_path=args.scenario,
        ssp_path=args.ssp,
        results_dir=args.results_dir,
        reuse_results=args.reuse_results,
        stop_time=args.stop_time,
        realtime=args.realtime,
        config_path=args.config_path,
        bridge_input=args.bridge_input,
    )
    print(json.dumps(scenario_result_summary(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
