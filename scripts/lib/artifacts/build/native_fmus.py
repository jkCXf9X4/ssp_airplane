#!/usr/bin/env python3
"""Build native shared libraries discovered from the SysML architecture."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, ensure_directory
from scripts.lib.artifacts.build import (
    DEFAULT_BUILD_ROOT,
    GENERATED_INTERFACE_DIR,
    GENERATED_MODEL_DESCRIPTION_DIR,
    NativeFmuProject,
    build_native_library,
    discover_native_projects,
    generated_model_description_paths,
)
from scripts.lib.artifacts.sysml_export.generate_c_interface_defs import generate_headers


def _discover_projects(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    build_root: Path = DEFAULT_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[NativeFmuProject]:
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


def build_flightgear_bridge_fmu(
    output_fmu: Path,
    build_dir: Path = DEFAULT_BUILD_ROOT / "flightgear_bridge",
) -> Path:
    from scripts.lib.artifacts.package import native_fmu as package_native_fmu_cli

    for project in discover_native_projects(build_root=DEFAULT_BUILD_ROOT):
        if project.model_identifier == "FlightGearBridge":
            project = NativeFmuProject(
                instance_name=project.instance_name,
                model_identifier=project.model_identifier,
                source_root=project.source_root,
                build_dir=build_dir,
            )
            build_native_libraries(
                architecture_path=ARCHITECTURE_DIR,
                build_root=DEFAULT_BUILD_ROOT,
                composition=COMPOSITION_NAME,
                models=[project.model_identifier],
            )
            return package_native_fmu_cli.package_native_fmu_for_project(
                project,
                output_fmu=output_fmu,
                build_dir=build_dir,
            )
    raise SystemExit("FlightGearBridge native project not found in architecture/model layout")


def parse_args(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--composition", default=COMPOSITION_NAME)
    parser.add_argument("--build-root", type=Path, default=DEFAULT_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to build, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    written = build_native_libraries(
        architecture_path=args.architecture,
        composition=args.composition,
        build_root=args.build_root,
        models=args.models,
    )
    if not written:
        print("No native projects discovered.")
        return 0
    for path in written:
        print(f"Built native library: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
