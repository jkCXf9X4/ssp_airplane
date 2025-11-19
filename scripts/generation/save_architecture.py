#!/usr/bin/env python3
"""Merge the SysML sections and emit a JSON snapshot of the architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from scripts.utils.sysml_helpers import load_architecture

DEFAULT_ARCH_DIR = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "arch_def.json"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_ARCH_DIR,
        help="Directory containing .sysml sections (or a file within).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to the JSON file that will store the merged architecture.",
    )
    args = parser.parse_args(argv)

    architecture = load_architecture(args.source)

    ensure_parent_dir(args.output)
    args.output.write_text(str(architecture))
    print(f"Architecture saved to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
