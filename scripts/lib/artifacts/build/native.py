"""Build native FMU shared libraries in an out-of-source build tree."""
from __future__ import annotations

import subprocess
from pathlib import Path

from scripts.lib.paths import (
    ARCHITECTURE_DIR,
    COMPOSITION_NAME,
    DEFAULT_NATIVE_BUILD_ROOT,
    GENERATED_INTERFACE_DIR,
    discover_native_projects,
    ensure_directory,
)


def build_native_fmus(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    build_root: Path = DEFAULT_NATIVE_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[Path]:
    from scripts.lib.artifacts.sysml_export.c_headers import generate_headers

    generate_headers(architecture_path, GENERATED_INTERFACE_DIR)
    projects = discover_native_projects(architecture_path, composition, build_root)
    if models:
        wanted = set(models)
        projects = [project for project in projects if project.model_identifier in wanted]

    built: list[Path] = []
    for project in projects:
        ensure_directory(project.build_dir)
        subprocess.run(
            ["cmake", "-S", str(project.source_root), "-B", str(project.build_dir)],
            check=True,
        )
        subprocess.run(["cmake", "--build", str(project.build_dir)], check=True)
        built.append(project.build_dir)
    return built
