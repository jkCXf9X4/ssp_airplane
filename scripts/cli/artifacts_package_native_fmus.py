#!/usr/bin/env python3
"""CLI for packaging native FMUs."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, DEFAULT_FMU_OUTPUT_DIR, DEFAULT_NATIVE_BUILD_ROOT


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package built native shared libraries into FMUs.")
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--composition", default=COMPOSITION_NAME)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_FMU_OUTPUT_DIR)
    parser.add_argument("--build-root", type=Path, default=DEFAULT_NATIVE_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to package, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    from scripts.lib.artifacts.package.native import package_native_fmus

    written = package_native_fmus(
        architecture_path=args.architecture,
        composition=args.composition,
        output_dir=args.output_dir,
        build_root=args.build_root,
        models=args.models,
    )
    if not written:
        print("No native projects discovered.")
        return 0
    for path in written:
        print(f"Packaged native FMU: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
