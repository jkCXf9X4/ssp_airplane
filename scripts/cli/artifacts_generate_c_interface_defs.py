#!/usr/bin/env python3
"""CLI for generating C and C++ interface definitions."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, GENERATED_DIR

DEFAULT_OUTPUT_DIR = GENERATED_DIR / "interfaces"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate native C/C++ interface headers.")
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from scripts.lib.artifacts.sysml_export.c_headers import generate_headers

    written = generate_headers(args.architecture, args.output_dir)
    print(f"Wrote {len(written)} interface headers to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
