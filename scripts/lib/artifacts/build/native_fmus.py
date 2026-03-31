#!/usr/bin/env python3
"""Build native FMUs discovered from the SysML architecture."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, ensure_directory
from scripts.lib.artifacts.build import (
    DEFAULT_BUILD_ROOT,
    DEFAULT_OUTPUT_DIR,
    GENERATED_INTERFACE_DIR,
    GENERATED_MODEL_DESCRIPTION_DIR,
    NativeFmuProject,
    build_native_library,
    discover_native_projects,
    generated_model_description_paths,
    package_native_fmu,
)
from scripts.lib.artifacts.sysml_export.generate_c_interface_defs import generate_headers


def build_native_fmu(
    project: NativeFmuProject,
    output_fmu: Path | None = None,
    build_dir: Path | None = None,
) -> Path:
    build_dir = build_dir or project.build_dir
    output_fmu = output_fmu or (DEFAULT_OUTPUT_DIR / project.output_name)

    if build_dir.exists():
        shutil.rmtree(build_dir)
    ensure_directory(build_dir)

    built_lib = build_native_library(project, build_dir)
    return package_native_fmu(project, built_lib, output_fmu, build_dir)


def build_native_fmus(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    build_root: Path = DEFAULT_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[Path]:
    projects = discover_native_projects(architecture_path, composition, build_root)
    if models:
        wanted = set(models)
        projects = [project for project in projects if project.model_identifier in wanted]

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
            build_native_fmu(
                project,
                output_fmu=output_dir / project.output_name,
                build_dir=project.build_dir,
            )
        )
    return written


def build_flightgear_bridge_fmu(
    output_fmu: Path = DEFAULT_OUTPUT_DIR / "FlightGearBridge.fmu",
    build_dir: Path = DEFAULT_BUILD_ROOT / "flightgear_bridge",
) -> Path:
    for project in discover_native_projects(build_root=DEFAULT_BUILD_ROOT):
        if project.model_identifier == "FlightGearBridge":
            project = NativeFmuProject(
                instance_name=project.instance_name,
                model_identifier=project.model_identifier,
                source_root=project.source_root,
                build_dir=build_dir,
            )
            generate_headers(ARCHITECTURE_DIR, GENERATED_INTERFACE_DIR)
            generated_model_description_paths(
                ARCHITECTURE_DIR,
                GENERATED_MODEL_DESCRIPTION_DIR,
                COMPOSITION_NAME,
            )
            return build_native_fmu(project, output_fmu=output_fmu, build_dir=build_dir)
    raise SystemExit("FlightGearBridge native project not found in architecture/model layout")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--composition", default=COMPOSITION_NAME)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--build-root", type=Path, default=DEFAULT_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to build, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    written = build_native_fmus(
        architecture_path=args.architecture,
        composition=args.composition,
        output_dir=args.output_dir,
        build_root=args.build_root,
        models=args.models,
    )
    if not written:
        print("No native FMUs discovered.")
        return 0
    for path in written:
        print(f"Built native FMU: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
