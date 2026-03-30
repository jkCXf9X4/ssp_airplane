#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pyssp_sysml2.ssd import generate_ssd

from scripts.common.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, GENERATED_DIR

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "SystemStructure.ssd"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Directory containing the SysML architecture (.sysml) files or a file within it.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--composition",
        default=COMPOSITION_NAME,
        help="Composition part definition to emit as an SSD.",
    )
    parser.add_argument(
        "--no-type-check",
        action="store_true",
        help="Skip strict source/destination port type equality checks during connection expansion.",
    )
    args = parser.parse_args(argv)

    try:
        output = generate_ssd(
            args.architecture,
            args.output,
            args.composition,
            type_check=not args.no_type_check,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(f"SSD written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
