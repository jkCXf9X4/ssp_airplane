"""Build native shared libraries for native FMU packaging."""
from __future__ import annotations

import shutil
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, FLIGHTGEAR_BRIDGE_MODEL_DIR, ensure_directory
from scripts.lib.artifacts.build.native_build import build_native_library
from scripts.lib.artifacts.build.native_discovery import (
    DEFAULT_BUILD_ROOT,
    GENERATED_INTERFACE_DIR,
    GENERATED_MODEL_DESCRIPTION_DIR,
    NativeFmuProject,
)


def _discover_projects(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    build_root: Path = DEFAULT_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[NativeFmuProject]:
    from scripts.lib.artifacts.build.native_discovery import discover_native_projects

    projects = discover_native_projects(architecture_path, composition, build_root)
    if models:
        wanted = set(models)
        projects = [project for project in projects if project.model_identifier in wanted]
    return projects


def build_native_library_for_project(
    project: NativeFmuProject,
    build_dir: Path | None = None,
) -> Path:
    build_dir = build_dir or project.build_dir

    if build_dir.exists():
        shutil.rmtree(build_dir)
    ensure_directory(build_dir)

    return build_native_library(project, build_dir)


def build_native_libraries(
    architecture_path: Path = ARCHITECTURE_DIR,
    build_root: Path = DEFAULT_BUILD_ROOT,
    composition: str = COMPOSITION_NAME,
    models: list[str] | None = None,
) -> list[Path]:
    from scripts.lib.artifacts.sysml_export.c_headers import generate_headers
    from scripts.lib.artifacts.sysml_export.model_description import generated_model_description_paths

    projects = _discover_projects(architecture_path, composition, build_root, models)
    if not projects:
        return []

    generate_headers(architecture_path, GENERATED_INTERFACE_DIR)
    generated_model_description_paths(
        architecture_path,
        GENERATED_MODEL_DESCRIPTION_DIR,
        composition,
    )

    written: list[Path] = []
    for project in projects:
        written.append(build_native_library_for_project(project, build_dir=project.build_dir))
    return written
