#!/usr/bin/env python3
"""CLI for generating Modelica interface definitions."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.artifacts.sysml_export.modelica_headers import (
    DEFAULT_ARCH_PATH,
    DEFAULT_OUTPUT_PATH,
    write_modelica_interfaces,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Modelica interface definitions.")
    parser.add_argument("--architecture", type=Path, default=DEFAULT_ARCH_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = write_modelica_interfaces(architecture_path=args.architecture, output=args.output)
    print(f"Wrote Modelica interfaces to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
