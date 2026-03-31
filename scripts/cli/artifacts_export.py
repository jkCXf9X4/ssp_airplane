#!/usr/bin/env python3
"""CLI for exporting all architecture-derived artifacts."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, GENERATED_DIR


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export all architecture-derived artifacts.")
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--generated-dir", type=Path, default=GENERATED_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from scripts.lib.artifacts.sysml_export.export import export_artifacts

    export_artifacts(architecture_path=args.architecture, generated_dir=args.generated_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
