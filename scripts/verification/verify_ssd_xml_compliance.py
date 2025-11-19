#!/usr/bin/env python3
"""Check that the generated SSD complies with the SSP XML schema."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pyssp_standard.ssd import SSD

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import GENERATED_DIR

DEFAULT_SSD_PATH = GENERATED_DIR / "SystemStructure.ssd"


def verify_ssd_xml(ssd_path: Path) -> int:
    if not ssd_path.exists():
        raise SystemExit(f"SSD file not found: {ssd_path}")
    with SSD(ssd_path) as handle:
        handle.__check_compliance__()
    print(f"SSD XML compliance verified for {ssd_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ssd",
        type=Path,
        default=DEFAULT_SSD_PATH,
        help="Path to the SystemStructure.ssd file to verify.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise SystemExit(verify_ssd_xml(args.ssd))


if __name__ == "__main__":
    main()
