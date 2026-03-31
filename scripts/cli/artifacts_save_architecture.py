#!/usr/bin/env python3
"""CLI for saving the merged architecture snapshot."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, GENERATED_DIR

DEFAULT_ARCH_DIR = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "arch_def.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a JSON snapshot of the architecture.")
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from scripts.lib.artifacts.sysml_export.architecture_snapshot import save_architecture

    output = save_architecture(source=args.source, output=args.output)
    print(f"Architecture saved to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
