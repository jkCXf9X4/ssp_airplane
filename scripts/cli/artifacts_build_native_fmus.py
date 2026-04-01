#!/usr/bin/env python3
"""CLI for building native FMU shared libraries."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, DEFAULT_NATIVE_BUILD_ROOT


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build native FMU shared libraries.")
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--composition", default=COMPOSITION_NAME)
    parser.add_argument("--build-root", type=Path, default=DEFAULT_NATIVE_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to build, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from scripts.lib.artifacts.build.native import build_native_fmus

    built = build_native_fmus(
        architecture_path=args.architecture,
        composition=args.composition,
        build_root=args.build_root,
        models=args.models,
    )
    if not built:
        print("No native projects discovered.")
        return 0
    for path in built:
        print(f"Built native project: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
