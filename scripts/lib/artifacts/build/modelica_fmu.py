#!/usr/bin/env python3
"""Build a single Modelica FMU from one or more package roots."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.modelica import run_omc
from scripts.lib.paths import BUILD_DIR, ensure_parent_dir


def build_mos_script(package_files: list[Path], model_name: str, work_dir: Path) -> str:
    load_files = "\n".join(f'loadFile("{path.as_posix()}");' for path in package_files)
    return f"""
installPackage(Modelica, "4.0.0", exactMatch=false);
{load_files}
cd("{work_dir.as_posix()}");
setCommandLineOptions("--fmiFlags=s:cvode");
setCommandLineOptions("--fmuRuntimeDepends=all");
filename := OpenModelica.Scripting.buildModelFMU({model_name}, version="2.0", fmuType="cs", platforms={{"static"}});
filename;
getErrorString();
"""


def extract_fmu_path(output: str) -> Path | None:
    matches = re.findall(r"\"([^\"]+\.fmu)\"", output)
    if not matches:
        return None
    return Path(matches[-1])


def build_modelica_fmu(package_files: list[Path], model_name: str, output_path: Path, omc_path: str, work_dir: Path) -> Path:
    ensure_parent_dir(output_path)
    work_dir.mkdir(parents=True, exist_ok=True)

    stdout = run_omc(omc_path, build_mos_script(package_files, model_name, work_dir))
    built_path = extract_fmu_path(stdout)
    if not built_path:
        raise SystemExit(f"Could not locate FMU emitted for {model_name}. omc output: {stdout}")

    output_path.unlink(missing_ok=True)
    try:
        shutil.move(str(built_path), output_path)
    except FileNotFoundError as exc:
        raise SystemExit(f"FMU file {built_path} missing after omc run for {model_name}") from exc
    return output_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-file", action="append", type=Path, required=True, help="Path to a package.mo file to load before building.")
    parser.add_argument("--model", required=True, help="Fully qualified Modelica class to export as an FMU.")
    parser.add_argument("--output", type=Path, required=True, help="Target FMU path.")
    parser.add_argument("--omc-path", default=os.environ.get("OMC", "omc"), help="Path to the omc executable.")
    parser.add_argument("--work-dir", type=Path, default=BUILD_DIR / "tmp", help="Directory where omc should emit the intermediate FMU.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = build_modelica_fmu(args.package_file, args.model, args.output, args.omc_path, args.work_dir)
    print(f"Built Modelica FMU: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
