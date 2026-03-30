#!/usr/bin/env python3
"""Build native FMUs that are implemented outside OpenModelica."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pyssp_sysml2.fmi import generate_model_descriptions

from scripts.common.paths import BUILD_DIR, COMPOSITION_NAME, FMI_HEADERS_DIR, FLIGHTGEAR_BRIDGE_MODEL_DIR, GENERATED_DIR, REPO_ROOT, ensure_directory, ensure_parent_dir
from scripts.generation.generate_c_interface_defs import common_header_name, generate_headers, part_header_name

NATIVE_ROOT = FLIGHTGEAR_BRIDGE_MODEL_DIR / "native"
DEFAULT_OUTPUT = BUILD_DIR / "fmus" / "Aircraft_FlightGearBridge.fmu"
DEFAULT_BUILD_DIR = BUILD_DIR / "native" / "flightgear_bridge"
MODEL_IDENTIFIER = "FlightGearBridge"
GENERATED_INTERFACE_DIR = REPO_ROOT / "generated" / "interfaces"
GENERATED_MODEL_DESCRIPTION_DIR = GENERATED_DIR / "model_descriptions"
GENERATED_COMMON_HEADER = GENERATED_INTERFACE_DIR / common_header_name("Aircraft")
GENERATED_MODEL_HEADER = GENERATED_INTERFACE_DIR / part_header_name("Aircraft", MODEL_IDENTIFIER)
FMI_HEADER_NAMES = ("fmi2TypesPlatform.h", "fmi2FunctionTypes.h", "fmi2Functions.h")


@dataclass(frozen=True)
class NativeFmuProject:
    name: str
    source_root: Path
    model_identifier: str
    binary_name: str
    build_dir: Path
    source_files: tuple[Path, ...]
    staged_files: tuple[Path, ...]


FLIGHTGEAR_BRIDGE_PROJECT = NativeFmuProject(
    name="FlightGearBridge",
    source_root=NATIVE_ROOT,
    model_identifier=MODEL_IDENTIFIER,
    binary_name=MODEL_IDENTIFIER,
    build_dir=DEFAULT_BUILD_DIR,
    source_files=(
        NATIVE_ROOT / "src" / "FlightGearBridge.cpp",
        NATIVE_ROOT / "src" / "BridgeRuntime.cpp",
        NATIVE_ROOT / "src" / "BridgeRuntime.hpp",
    ),
    staged_files=(
        NATIVE_ROOT / "src" / "FlightGearBridge.cpp",
        NATIVE_ROOT / "src" / "BridgeRuntime.cpp",
        NATIVE_ROOT / "src" / "BridgeRuntime.hpp",
        GENERATED_COMMON_HEADER,
        GENERATED_MODEL_HEADER,
        *(FMI_HEADERS_DIR / name for name in FMI_HEADER_NAMES),
    ),
)


def _generated_model_description_path() -> Path:
    generate_model_descriptions(
        REPO_ROOT / "architecture",
        GENERATED_MODEL_DESCRIPTION_DIR,
        COMPOSITION_NAME,
    )
    return GENERATED_MODEL_DESCRIPTION_DIR / MODEL_IDENTIFIER / "modelDescription.xml"


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

    built_lib = build_dir / f"{project.binary_name}.so"
    if not built_lib.exists():
        raise SystemExit(f"Native bridge library not found: {built_lib}")
    return built_lib


def build_flightgear_bridge_fmu(output_fmu: Path = DEFAULT_OUTPUT, build_dir: Path = DEFAULT_BUILD_DIR) -> Path:
    stage_dir = build_dir / "stage"
    binary_dir = stage_dir / "binaries" / "linux64"
    source_dir = stage_dir / "sources"

    generate_headers(REPO_ROOT / "architecture", GENERATED_INTERFACE_DIR)
    model_description_path = _generated_model_description_path()

    if build_dir.exists():
        shutil.rmtree(build_dir)
    ensure_directory(build_dir)
    ensure_directory(binary_dir)
    ensure_directory(source_dir)

    built_lib = _build_native_library(FLIGHTGEAR_BRIDGE_PROJECT, build_dir)

    shutil.copy2(built_lib, binary_dir / f"{MODEL_IDENTIFIER}.so")
    shutil.copy2(model_description_path, stage_dir / "modelDescription.xml")
    for path in FLIGHTGEAR_BRIDGE_PROJECT.staged_files:
        shutil.copy2(path, source_dir / path.name)

    ensure_parent_dir(output_fmu)
    with zipfile.ZipFile(output_fmu, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage_dir.rglob("*")):
            if path.is_dir():
                continue
            archive.write(path, arcname=path.relative_to(stage_dir).as_posix())

    return output_fmu


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--build-dir", type=Path, default=DEFAULT_BUILD_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = build_flightgear_bridge_fmu(args.output, args.build_dir)
    print(f"Built native FMU: {output}")


if __name__ == "__main__":
    main()
