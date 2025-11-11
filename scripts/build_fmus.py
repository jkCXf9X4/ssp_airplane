#!/usr/bin/env python3
"""Compile Modelica models into FMUs using OpenModelica's omc CLI."""
from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODELS = [
    "SSPAirplane.Fuselage",
    "SSPAirplane.ReactorCore",
    "SSPAirplane.WingSystem",
    "SSPAirplane.MotorArray",
    "SSPAirplane.ControlSoftware",
    "SSPAirplane.AutopilotModule",
    "SSPAirplane.ElectricalSystem",
    "SSPAirplane.AircraftSystem",
]


def build_mos_script(model_name: str, output_dir: Path) -> str:
    package_path = REPO_ROOT / "models" / "SSPAirplane" / "package.mo"
    return f"""
loadModel(Modelica);
loadFile("{package_path.as_posix()}");
setCommandLineOptions("+simCodeTarget=omsic +d=initialization");
buildModelFMU({model_name}, version="2.0", includeResources=true,
  platforms={{"static"}}, outputDirectory="{output_dir.as_posix()}" );
getErrorString();
"""


def run_omc(omc_path: str, mos_content: str, dry_run: bool = False) -> None:
    if dry_run:
        print("[dry-run] Would invoke omc with script:\n" + mos_content)
        return

    with tempfile.NamedTemporaryFile("w", suffix=".mos", delete=False) as handle:
        handle.write(mos_content)
        mos_file = Path(handle.name)

    try:
        subprocess.run([omc_path, str(mos_file)], check=True, cwd=REPO_ROOT)
    except FileNotFoundError as exc:
        raise SystemExit(
            "omc executable not found. Install OpenModelica or pass --omc-path"
        ) from exc
    finally:
        mos_file.unlink(missing_ok=True)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


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
        default=REPO_ROOT / "build" / "fmus",
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
    ensure_dir(output_dir)

    for model in args.models:
        mos_script = build_mos_script(model, output_dir)
        print(f"Exporting {model} -> {output_dir}")
        run_omc(args.omc_path, mos_script, dry_run=args.dry_run)

    print("FMU build process finished.")


if __name__ == "__main__":
    main()
