#!/usr/bin/env python3
"""CLI for evaluating scenario results against requirements."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.lib.scenarios.results import analyze_scenario_results, scenario_result_payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a scenario results CSV against requirement metrics.")
    parser.add_argument("--scenario", type=Path, required=True, help="Path to scenario JSON file.")
    parser.add_argument("--results-csv", type=Path, required=True, help="Path to the simulation results CSV.")
    parser.add_argument(
        "--summary-path",
        type=Path,
        default=None,
        help="Optional path to write the requirement summary JSON.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = analyze_scenario_results(
        scenario_path=args.scenario,
        result_file=args.results_csv,
        summary_path=args.summary_path,
    )
    print(json.dumps(scenario_result_payload(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
