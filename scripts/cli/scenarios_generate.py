#!/usr/bin/env python3
"""CLI for randomized scenario generation."""
from __future__ import annotations

import argparse

from pathlib import Path

from scripts.lib.scenarios.generate import write_scenario


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a randomized scenario JSON file.")
    parser.add_argument("--output", type=Path, required=True, help="Destination JSON file.")
    parser.add_argument("--points", type=int, default=None, help="Number of scenario points (3-10).")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed.")
    parser.add_argument("--min-distance", type=float, default=100.0)
    parser.add_argument("--max-distance", type=float, default=1000.0)
    parser.add_argument("--min-altitude", type=float, default=100.0)
    parser.add_argument("--max-altitude", type=float, default=10000.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    scenario = write_scenario(
        output=args.output,
        points=args.points,
        seed=args.seed,
        min_distance_km=args.min_distance,
        max_distance_km=args.max_distance,
        min_altitude_m=args.min_altitude,
        max_altitude_m=args.max_altitude,
    )
    print(f"Wrote scenario with {len(scenario['points'])} points to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
