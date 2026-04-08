#!/usr/bin/env python3
"""CLI for packaging an SSP with a scenario parameter set."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.lib.scenarios.packaging import package_ssp_with_parameters
from scripts.lib.scenarios.preparation import DEFAULT_RESULTS, DEFAULT_SSP


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inject a parameter set into an SSP archive.")
    parser.add_argument("--ssp", type=Path, default=DEFAULT_SSP, help="Path to the SSP archive.")
    parser.add_argument("--parameter-set", type=Path, required=True, help="Path to the waypoint parameter set (.ssv).")
    parser.add_argument(
        "--scenario-stem",
        required=True,
        help="Scenario stem used for naming the prepared SSP run directory and archive.",
    )
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS, help="Directory for generated artifacts.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    prepared_ssp = package_ssp_with_parameters(
        ssp_path=args.ssp,
        parameter_set_path=args.parameter_set,
        scenario_stem=args.scenario_stem,
        results_dir=args.results_dir,
    )
    print(
        json.dumps(
            {
                "ssp": str(args.ssp),
                "parameter_set": str(args.parameter_set),
                "prepared_ssp": str(prepared_ssp),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
