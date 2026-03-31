#!/usr/bin/env python3
"""CLI for OpenModelica equation checks."""
from __future__ import annotations

import argparse

from scripts.lib.verify.model_equations import DEFAULT_MODELS, verify_models


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run OpenModelica model equation checks.")
    parser.add_argument("--omc", default="omc", help="Path to the omc executable.")
    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_MODELS,
        help="Fully qualified Modelica classes to check.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return verify_models(args.omc, args.models)


if __name__ == "__main__":
    raise SystemExit(main())
