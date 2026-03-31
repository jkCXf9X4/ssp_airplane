#!/usr/bin/env python3
"""CLI for packaging the SSP archive."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.artifacts.package.ssp import DEFAULT_FMU_DIR, DEFAULT_OUTPUT, DEFAULT_SSD, package_ssp


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package FMUs and the SSD into an SSP archive.")
    parser.add_argument("--fmu-dir", type=Path, default=DEFAULT_FMU_DIR)
    parser.add_argument("--ssd", type=Path, default=DEFAULT_SSD)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = package_ssp(fmu_dir=args.fmu_dir, ssd=args.ssd, output=args.output)
    print(f"Packaged SSP written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
