#!/usr/bin/env python3
"""CLI for SSD XML compliance checks."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.verify.ssd_xml import DEFAULT_SSD_PATH, verify_ssd_xml


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate SSD XML compliance.")
    parser.add_argument(
        "--ssd",
        type=Path,
        default=DEFAULT_SSD_PATH,
        help="Path to the SystemStructure.ssd file to verify.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return verify_ssd_xml(args.ssd)


if __name__ == "__main__":
    raise SystemExit(main())
