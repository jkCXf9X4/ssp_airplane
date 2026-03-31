"""Native FMU staging, packaging, and packaging CLI."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys
import zipfile

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, FMI_HEADERS_DIR, ensure_directory, ensure_parent_dir
from scripts.lib.artifacts.build import DEFAULT_BUILD_ROOT, DEFAULT_OUTPUT_DIR, GENERATED_INTERFACE_DIR, GENERATED_MODEL_DESCRIPTION_DIR
from scripts.lib.artifacts.build.native_fmu_discovery import discover_native_projects
from scripts.lib.artifacts.build.native_fmu_project import NativeFmuProject
from scripts.lib.artifacts.sysml_export.generate_c_interface_defs import generate_headers
from scripts.lib.artifacts.sysml_export.native_fmu import generated_model_description_paths

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
    build_root: Path = DEFAULT_BUILD_ROOT,
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
        if path.is_file() and "CMakeFiles" not in path.parts
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


def package_native_fmu_for_project(
    project: NativeFmuProject,
    output_fmu: Path | None = None,
    build_dir: Path | None = None,
) -> Path:
    build_dir = build_dir or project.build_dir
    output_fmu = output_fmu or (DEFAULT_OUTPUT_DIR / project.output_name)
    built_library = find_built_library(project, build_dir)
    return package_native_fmu(project, built_library, output_fmu, build_dir)


def package_native_fmus(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    build_root: Path = DEFAULT_BUILD_ROOT,
    models: list[str] | None = None,
) -> list[Path]:
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
                build_dir=project.build_dir,
            )
        )
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--composition", default=COMPOSITION_NAME)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--build-root", type=Path, default=DEFAULT_BUILD_ROOT)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Optional part definition names to package, for example FlightGearBridge",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    written = package_native_fmus(
        architecture_path=args.architecture,
        composition=args.composition,
        output_dir=args.output_dir,
        build_root=args.build_root,
        models=args.models,
    )
    if not written:
        print("No native projects discovered.")
        return 0
    for path in written:
        print(f"Packaged native FMU: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
