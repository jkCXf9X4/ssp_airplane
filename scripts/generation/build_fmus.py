#!/usr/bin/env python3
"""Compile Modelica models into FMUs using OpenModelica's omc CLI."""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.modelica_specs import DEFAULT_MODELICA_MODELS, spec_by_model_name
from scripts.common.paths import BUILD_DIR, ensure_directory
from scripts.generation.build_modelica_fmu import build_modelica_fmu
from scripts.generation.build_native_fmus import build_flightgear_bridge_fmu
DEFAULT_MODELS = DEFAULT_MODELICA_MODELS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_MODELS,
        help="Fully qualified Modelica classes to export as FMUs",
    )
    parser.add_argument(
        "--omc-path",
        default=os.environ.get("OMC", "omc"),
        help="Path to the omc executable",
    )
    parser.add_argument(
        "--output",
        default=BUILD_DIR / "fmus",
        type=Path,
        help="Destination directory for FMUs",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print omc commands without executing them",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    ensure_directory(output_dir)

    for model in args.models:
        print(f"Exporting {model} -> {output_dir}")
        spec = spec_by_model_name(model)
        if args.dry_run:
            print(f"[dry-run] Would build {model} from {[path.as_posix() for path in spec.package_files]}")
            continue
        target_path = output_dir / f"{spec.output_name}.fmu"
        work_dir = BUILD_DIR / "tmp" / spec.folder_name
        build_modelica_fmu(spec.package_files, spec.model_name, target_path, args.omc_path, work_dir)
        print(f"  -> {target_path}")

    native_fmu = build_flightgear_bridge_fmu(output_dir / "Aircraft_FlightGearBridge.fmu")
    print(f"  -> {native_fmu}")

    print("FMU build process finished.")


if __name__ == "__main__":
    main()
