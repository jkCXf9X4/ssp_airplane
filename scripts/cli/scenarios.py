#!/usr/bin/env python3
"""Scenario-oriented commands."""
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("generate", help="Generate a randomized scenario JSON file.")
    subparsers.add_parser("simulate", help="Run or reuse a scenario simulation.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, remaining = parser.parse_known_args(argv)
    if args.command == "generate":
        from scripts.lib.scenarios import generate_scenario

        return generate_scenario.main(remaining)
    if args.command == "simulate":
        from scripts.lib.scenarios import simulate_scenario

        return simulate_scenario.main(remaining)
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
