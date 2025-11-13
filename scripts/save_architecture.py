#!/usr/bin/env python3
"""Merge the SysML sections and emit a JSON snapshot of the architecture."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from utils.sysmlv2_arch_parser import parse_sysml_folder

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCH_DIR = REPO_ROOT / "architecture"
DEFAULT_OUTPUT = REPO_ROOT / "generated" / "arch_def.json"


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

    source = args.source
    if source.is_file():
        source = source.parent
    architecture = parse_sysml_folder(source)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(str(architecture))
    print(f"Architecture saved to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
