#!/usr/bin/env python3
"""CLI for building native FMU shared libraries."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, BUILD_DIR, COMPOSITION_NAME

DEFAULT_BUILD_ROOT = BUILD_DIR / "native"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build only native shared libraries.")
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--composition", default=COMPOSITION_NAME)
    parser.add_argument("--build-root", type=Path, default=DEFAULT_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to build, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from scripts.lib.artifacts.build.native import build_native_libraries

    written = build_native_libraries(
        architecture_path=args.architecture,
        composition=args.composition,
        build_root=args.build_root,
        models=args.models,
    )
    if not written:
        print("No native projects discovered.")
        return 0
    for path in written:
        print(f"Built native library: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
