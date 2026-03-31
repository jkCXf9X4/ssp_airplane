#!/usr/bin/env python3
"""CLI for SysML versus Modelica interface verification."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Modelica interface variables against SysML.")
    parser.add_argument(
        "--architecture",
        type=Path,
        default=ARCHITECTURE_DIR,
        help="Path to the SysML architecture directory or file.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from scripts.lib.verify.modelica_variables import verify_modelica_variables

    return verify_modelica_variables(args.architecture)


if __name__ == "__main__":
    raise SystemExit(main())
