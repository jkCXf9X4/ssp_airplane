#!/usr/bin/env python3
"""Build one or more Modelica FMUs from package roots."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.modelica import DEFAULT_MODELICA_MODELS, run_omc, spec_by_model_name
from scripts.lib.paths import BUILD_DIR, ensure_directory, ensure_parent_dir


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


def build_modelica_fmus(
    models: list[str] | None = None,
    output_dir: Path = BUILD_DIR / "fmus",
    omc_path: str = os.environ.get("OMC", "omc"),
    dry_run: bool = False,
) -> list[Path]:
    ensure_directory(output_dir)

    written: list[Path] = []
    for model in models or DEFAULT_MODELICA_MODELS:
        spec = spec_by_model_name(model)
        target_path = output_dir / f"{spec.output_name}.fmu"
        work_dir = BUILD_DIR / "tmp" / spec.folder_name
        if dry_run:
            print(f"[dry-run] Would build {model} from {[path.as_posix() for path in spec.package_files]}")
            continue
        print(f"Exporting {model} -> {target_path}")
        written.append(
            build_modelica_fmu(
                spec.package_files,
                spec.model_name,
                target_path,
                omc_path,
                work_dir,
            )
        )
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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
