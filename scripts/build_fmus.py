#!/usr/bin/env python3
"""Compile Modelica models into FMUs using OpenModelica's omc CLI."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODELS = [
    "Aircraft.CompositeAirframe",
    "Aircraft.TurbofanPropulsion",
    "Aircraft.AdaptiveWingSystem",
    "Aircraft.MissionComputer",
    "Aircraft.AutopilotModule",
    "Aircraft.InputOutput",
    "Aircraft.PowerSystem",
    "Aircraft.FuelSystem",
    "Aircraft.ControlInterface",
    "Aircraft.AirDataAndInertialSuite",
    "Aircraft.EmergencyPowerUnit",
    "Aircraft.FlyByWireController",
    "Aircraft.StructuralLoadsAndPerformanceMonitor",
    "Aircraft.StoresManagementSystem",
]


def build_mos_script(model_name: str, output_dir: Path) -> str:
    package_path = REPO_ROOT / "models" / "Aircraft" / "package.mo"
    tmp_dir = REPO_ROOT / "build/tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return f"""
loadFile("{package_path.as_posix()}");
cd("./build/tmp/");
setCommandLineOptions("--fmiFlags=s:cvode");
setCommandLineOptions("--fmuRuntimeDepends=all");
filename := OpenModelica.Scripting.buildModelFMU({model_name}, version="2.0", fmuType="cs", platforms={{"static"}});
filename;
getErrorString();
"""


def run_omc(omc_path: str, mos_content: str, dry_run: bool = False) -> str:
    if dry_run:
        print("[dry-run] Would invoke omc with script:\n" + mos_content)
        return ""

    with tempfile.NamedTemporaryFile("w", suffix=".mos", delete=False) as handle:
        handle.write(mos_content)
        mos_file = Path(handle.name)

    try:
        proc = subprocess.run(
            [omc_path, str(mos_file)],
            check=True,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit(
            "omc executable not found. Install OpenModelica or pass --omc-path"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.stderr or exc.stdout) from exc
    finally:
        mos_file.unlink(missing_ok=True)

    if proc.stderr:
        print(proc.stderr.strip())
    return proc.stdout


def extract_fmu_path(output: str) -> Path | None:
    matches = re.findall(r"\"([^\"]+\.fmu)\"", output)
    if not matches:
        return None
    return Path(matches[-1])


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

    if output_dir.exists():
        shutil.rmtree(output_dir)
    ensure_dir(output_dir)

    for model in args.models:
        mos_script = build_mos_script(model, output_dir)
        print(f"Exporting {model} -> {output_dir}")
        stdout = run_omc(args.omc_path, mos_script, dry_run=args.dry_run)
        if args.dry_run:
            continue
        built_path = extract_fmu_path(stdout)
        if not built_path:
            raise SystemExit(f"Could not locate FMU emitted for {model}. omc output: {stdout}")
        target_name = model.replace(".", "_") + ".fmu"
        target_path = output_dir / target_name
        try:
            target_path.unlink(missing_ok=True)
            shutil.move(str(built_path), target_path)
        except FileNotFoundError as exc:
            raise SystemExit(f"FMU file {built_path} missing after omc run for {model}") from exc
        print(f"  -> {target_path}")

    print("FMU build process finished.")


if __name__ == "__main__":
    main()
