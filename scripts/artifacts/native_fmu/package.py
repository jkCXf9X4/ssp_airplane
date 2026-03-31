"""Native FMU staging and packaging helpers."""
from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

from scripts.common.paths import FMI_HEADERS_DIR, ensure_directory, ensure_parent_dir
from scripts.artifacts.native_fmu.projects import NativeFmuProject

FMI_HEADER_NAMES = ("fmi2TypesPlatform.h", "fmi2FunctionTypes.h", "fmi2Functions.h")


def stage_native_fmu_sources(project: NativeFmuProject, source_dir: Path) -> None:
    for path in sorted(project.source_root.rglob("*")):
        if path.is_dir():
            continue
        target = source_dir / path.relative_to(project.source_root)
        ensure_parent_dir(target)
        shutil.copy2(path, target)

    generated_targets = {
        project.generated_common_header: source_dir / "generated" / project.generated_common_header.name,
        project.generated_model_header: source_dir / "generated" / project.generated_model_header.name,
    }
    for header_name in FMI_HEADER_NAMES:
        source = FMI_HEADERS_DIR / header_name
        generated_targets[source] = source_dir / "include" / header_name

    for source, target in generated_targets.items():
        ensure_parent_dir(target)
        shutil.copy2(source, target)


def package_native_fmu(
    project: NativeFmuProject,
    built_library: Path,
    output_fmu: Path,
    build_dir: Path,
) -> Path:
    stage_dir = build_dir / "stage"
    binary_dir = stage_dir / "binaries" / "linux64"
    source_dir = stage_dir / "sources"

    ensure_directory(binary_dir)
    ensure_directory(source_dir)

    shutil.copy2(built_library, binary_dir / f"{project.model_identifier}.so")
    shutil.copy2(project.model_description_path, stage_dir / "modelDescription.xml")
    stage_native_fmu_sources(project, source_dir)

    ensure_parent_dir(output_fmu)
    with zipfile.ZipFile(output_fmu, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage_dir.rglob("*")):
            if path.is_dir():
                continue
            archive.write(path, arcname=path.relative_to(stage_dir).as_posix())

    return output_fmu
