"""Build standalone Modelica FMUs."""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from scripts.lib.common.modelica import DEFAULT_MODELICA_MODELS, run_omc, spec_by_model_name
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
