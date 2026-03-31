#!/usr/bin/env python3
"""CLI for building Modelica FMUs."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from scripts.lib.artifacts.build.modelica import build_modelica_fmu, build_modelica_fmus
from scripts.lib.paths import BUILD_DIR


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build only Modelica FMUs.")
    parser.add_argument("--package-file", action="append", type=Path, help="Path to a package.mo file to load before building.")
    parser.add_argument("--model", help="Fully qualified Modelica class to export as an FMU.")
    parser.add_argument("--models", nargs="+", help="Fully qualified Modelica classes to export as FMUs.")
    parser.add_argument("--output", type=Path, help="Target FMU path.")
    parser.add_argument("--output-dir", type=Path, default=BUILD_DIR / "fmus", help="Target directory for multiple FMUs.")
    parser.add_argument("--omc-path", default=os.environ.get("OMC", "omc"), help="Path to the omc executable.")
    parser.add_argument("--work-dir", type=Path, default=BUILD_DIR / "tmp", help="Directory where omc should emit the intermediate FMU.")
    parser.add_argument("--dry-run", action="store_true", help="Print build actions without running omc.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.package_file or args.model or args.output:
        if not (args.package_file and args.model and args.output):
            raise SystemExit("--package-file, --model, and --output must be provided together")
        output = build_modelica_fmu(args.package_file, args.model, args.output, args.omc_path, args.work_dir)
        print(f"Built Modelica FMU: {output}")
        return 0

    written = build_modelica_fmus(
        models=args.models,
        output_dir=args.output_dir,
        omc_path=args.omc_path,
        dry_run=args.dry_run,
    )
    for path in written:
        print(f"Built Modelica FMU: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
