#!/usr/bin/env python3
"""Build native FMUs discovered from the SysML architecture."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
import re

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pycps_sysmlv2 import NodeType, SysMLParser

from scripts.common.paths import ARCHITECTURE_DIR, BUILD_DIR, COMPOSITION_NAME, FMI_HEADERS_DIR, GENERATED_DIR, MODELS_DIR, REPO_ROOT, ensure_directory, ensure_parent_dir
from scripts.generation.generate_c_interface_defs import common_header_name, generate_headers, part_header_name
from scripts.generation.generate_model_descriptions import generate_model_descriptions

DEFAULT_OUTPUT_DIR = BUILD_DIR / "fmus"
DEFAULT_BUILD_ROOT = BUILD_DIR / "native"
GENERATED_INTERFACE_DIR = REPO_ROOT / "generated" / "interfaces"
GENERATED_MODEL_DESCRIPTION_DIR = GENERATED_DIR / "model_descriptions"
FMI_HEADER_NAMES = ("fmi2TypesPlatform.h", "fmi2FunctionTypes.h", "fmi2Functions.h")


@dataclass(frozen=True)
class NativeFmuProject:
    instance_name: str
    model_identifier: str
    source_root: Path
    build_dir: Path

    @property
    def output_name(self) -> str:
        return f"Aircraft_{self.model_identifier}.fmu"

    @property
    def generated_model_header(self) -> Path:
        return GENERATED_INTERFACE_DIR / part_header_name("Aircraft", self.model_identifier)

    @property
    def generated_common_header(self) -> Path:
        return GENERATED_INTERFACE_DIR / common_header_name("Aircraft")

    @property
    def model_description_path(self) -> Path:
        return GENERATED_MODEL_DESCRIPTION_DIR / self.model_identifier / "modelDescription.xml"


def _snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def discover_native_projects(
    architecture_path: Path = ARCHITECTURE_DIR,
    composition: str = COMPOSITION_NAME,
    build_root: Path = DEFAULT_BUILD_ROOT,
) -> list[NativeFmuProject]:
    system = SysMLParser(architecture_path).parse().get_def(NodeType.Part, composition)
    projects: list[NativeFmuProject] = []
    for instance_name, part_ref in system.refs(NodeType.Part).items():
        folder_name = instance_name
        source_root = MODELS_DIR / folder_name / "native"
        if not (source_root / "CMakeLists.txt").exists():
            folder_name = _snake_case(part_ref.type)
            source_root = MODELS_DIR / folder_name / "native"
        if not (source_root / "CMakeLists.txt").exists():
            continue
        projects.append(
            NativeFmuProject(
                instance_name=instance_name,
                model_identifier=part_ref.type,
                source_root=source_root,
                build_dir=build_root / folder_name,
            )
        )
    return projects


def _generated_model_description_paths(
    architecture_path: Path,
    output_dir: Path,
    composition: str,
) -> dict[str, Path]:
    written = generate_model_descriptions(
        architecture_path,
        output_dir,
        composition,
    )
    return {path.parent.name: path for path in written}


def _build_native_library(project: NativeFmuProject, build_dir: Path) -> Path:
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


def _stage_project_sources(project: NativeFmuProject, source_dir: Path) -> None:
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


def build_native_fmu(
    project: NativeFmuProject,
    output_fmu: Path | None = None,
    build_dir: Path | None = None,
) -> Path:
    build_dir = build_dir or project.build_dir
    output_fmu = output_fmu or (DEFAULT_OUTPUT_DIR / project.output_name)

    stage_dir = build_dir / "stage"
    binary_dir = stage_dir / "binaries" / "linux64"
    source_dir = stage_dir / "sources"

    if build_dir.exists():
        shutil.rmtree(build_dir)
    ensure_directory(build_dir)
    ensure_directory(binary_dir)
    ensure_directory(source_dir)

    built_lib = _build_native_library(project, build_dir)

    shutil.copy2(built_lib, binary_dir / f"{project.model_identifier}.so")
    shutil.copy2(project.model_description_path, stage_dir / "modelDescription.xml")
    _stage_project_sources(project, source_dir)

    ensure_parent_dir(output_fmu)
    with zipfile.ZipFile(output_fmu, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage_dir.rglob("*")):
            if path.is_dir():
                continue
            archive.write(path, arcname=path.relative_to(stage_dir).as_posix())

    return output_fmu


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
    model_descriptions = _generated_model_description_paths(
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
    output_fmu: Path = DEFAULT_OUTPUT_DIR / "Aircraft_FlightGearBridge.fmu",
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
            _generated_model_description_paths(
                ARCHITECTURE_DIR,
                GENERATED_MODEL_DESCRIPTION_DIR,
                COMPOSITION_NAME,
            )
            return build_native_fmu(project, output_fmu=output_fmu, build_dir=build_dir)
    raise SystemExit("FlightGearBridge native project not found in architecture/model layout")


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    written = build_native_fmus(
        architecture_path=args.architecture,
        composition=args.composition,
        output_dir=args.output_dir,
        build_root=args.build_root,
        models=args.models,
    )
    if not written:
        print("No native FMUs discovered.")
        return
    for path in written:
        print(f"Built native FMU: {path}")


if __name__ == "__main__":
    main()
