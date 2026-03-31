#!/usr/bin/env python3
"""CLI for generating analysis plots."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.lib.results.plots import generate_plots


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate plots from a simulation results CSV.")
    parser.add_argument("--results-csv", type=Path, required=True, help="Path to the simulation results CSV.")
    parser.add_argument(
        "--scenario",
        type=Path,
        default=None,
        help="Optional scenario JSON to overlay waypoints on the flight-path plots.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write plots (defaults to the results CSV directory).",
    )
    parser.add_argument("--plot-path", action="store_true", help="Generate the 2D flight-path plot.")
    parser.add_argument("--plot-3d", action="store_true", help="Generate the 3D flight-path plot.")
    parser.add_argument(
        "--plot-fuel-altitude",
        action="store_true",
        help="Generate the fuel remaining and altitude versus time plot.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    print(
        json.dumps(
            generate_plots(
                results_csv=args.results_csv,
                scenario=args.scenario,
                output_dir=args.output_dir,
                plot_path=args.plot_path,
                plot_3d=args.plot_3d,
                plot_fuel_altitude=args.plot_fuel_altitude,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
