"""Build native shared libraries for native FMU packaging."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, REPO_ROOT, ensure_directory
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


def build_native_library(project: NativeFmuProject, build_dir: Path) -> Path:
    subprocess.run(
        ["cmake", "-S", str(project.source_root), "-B", str(build_dir), "-DCMAKE_BUILD_TYPE=Release"],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(
        ["cmake", "--build", str(build_dir), "--config", "Release"],
        check=True,
        cwd=REPO_ROOT,
    )

    candidates = sorted(
        path for path in build_dir.rglob("*.so")
        if path.is_file() and "CMakeFiles" not in path.parts
    )
    if not candidates:
        raise SystemExit(f"Native library not found under {build_dir}")
    if len(candidates) == 1:
        return candidates[0]

    exact_matches = [path for path in candidates if path.stem == project.model_identifier]
    if len(exact_matches) == 1:
        return exact_matches[0]
    raise SystemExit(
        f"Expected one native library for {project.model_identifier}, found: {[path.name for path in candidates]}"
    )


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
