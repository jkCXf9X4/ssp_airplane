"""Package built native libraries into native FMUs."""
from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

from scripts.lib.paths import (
    ARCHITECTURE_DIR,
    COMPOSITION_NAME,
    DEFAULT_FMU_OUTPUT_DIR,
    DEFAULT_NATIVE_BUILD_ROOT,
    FMI_HEADERS_DIR,
    GENERATED_INTERFACE_DIR,
    GENERATED_MODEL_DESCRIPTION_DIR,
    NativeFmuProject,
    REPO_ROOT,
    discover_native_projects,
    ensure_directory,
    ensure_parent_dir,
)

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


def _discover_projects(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    build_root: Path = DEFAULT_NATIVE_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[NativeFmuProject]:
    projects = discover_native_projects(architecture_path, composition, build_root)
    if models:
        wanted = set(models)
        projects = [project for project in projects if project.model_identifier in wanted]
    return projects


def find_built_library(project: NativeFmuProject, build_dir: Path) -> Path:
    candidates = sorted(
        path for path in build_dir.rglob("*.so")
        if path.is_file() and "CMakeFiles" not in path.parts and "stage" not in path.parts
    )
    if not candidates:
        raise SystemExit(f"Native library not found under {build_dir}")
    exact_matches = [path for path in candidates if path.stem == project.model_identifier]
    if len(exact_matches) == 1:
        return exact_matches[0]
    if len(candidates) == 1:
        return candidates[0]
    raise SystemExit(
        f"Expected one native library for {project.model_identifier}, found: {[path.name for path in candidates]}"
    )


def candidate_build_dirs(project: NativeFmuProject, build_root: Path) -> list[Path]:
    candidates = [project.build_dir]
    try:
        source_relative = project.source_root.relative_to(REPO_ROOT)
    except ValueError:
        return candidates

    top_level_cmake_dir = build_root / source_relative
    if top_level_cmake_dir not in candidates:
        candidates.append(top_level_cmake_dir)
    return candidates


def package_native_fmu_for_project(
    project: NativeFmuProject,
    output_fmu: Path | None = None,
    build_dir: Path | None = None,
    build_root: Path = DEFAULT_NATIVE_BUILD_ROOT,
) -> Path:
    resolved_build_dir = build_dir
    if resolved_build_dir is None:
        for candidate in candidate_build_dirs(project, build_root):
            try:
                find_built_library(project, candidate)
            except SystemExit:
                continue
            resolved_build_dir = candidate
            break
    if resolved_build_dir is None:
        searched = ", ".join(str(path) for path in candidate_build_dirs(project, build_root))
        raise SystemExit(f"Native library not found for {project.model_identifier}. Searched: {searched}")

    output_fmu = output_fmu or (DEFAULT_FMU_OUTPUT_DIR / project.output_name)
    built_library = find_built_library(project, resolved_build_dir)
    return package_native_fmu(project, built_library, output_fmu, resolved_build_dir)


def package_native_fmus(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    output_dir: Path = DEFAULT_FMU_OUTPUT_DIR,
    build_root: Path = DEFAULT_NATIVE_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[Path]:
    from scripts.lib.artifacts.sysml_export.c_headers import generate_headers
    from scripts.lib.artifacts.sysml_export.model_description import generated_model_description_paths

    projects = _discover_projects(architecture_path, composition, build_root, models)
    if not projects:
        return []

    ensure_directory(output_dir)
    generate_headers(architecture_path, GENERATED_INTERFACE_DIR)
    model_descriptions = generated_model_description_paths(
        architecture_path,
        GENERATED_MODEL_DESCRIPTION_DIR,
        composition,
    )

    written: list[Path] = []
    for project in projects:
        if project.model_identifier not in model_descriptions:
            raise SystemExit(f"modelDescription.xml not generated for {project.model_identifier}")
        written.append(
            package_native_fmu_for_project(
                project,
                output_fmu=output_dir / project.output_name,
                build_root=build_root,
            )
        )
    return written
