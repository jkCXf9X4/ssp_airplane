#!/usr/bin/env python3
"""CLI for building the FlightGear bridge FMU."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.artifacts.build.native import build_flightgear_bridge_fmu
from scripts.lib.artifacts.build.native_project import DEFAULT_BUILD_ROOT


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build only the FlightGear bridge FMU.")
    parser.add_argument("--output", type=Path, required=True, help="Target FMU path.")
    parser.add_argument("--build-dir", type=Path, default=DEFAULT_BUILD_ROOT / "flightgear_bridge", help="Build directory for the native FMU.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = build_flightgear_bridge_fmu(output_fmu=args.output, build_dir=args.build_dir)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
