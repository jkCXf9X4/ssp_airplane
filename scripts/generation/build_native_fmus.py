#!/usr/bin/env python3
"""Build native FMUs that are implemented outside OpenModelica."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import BUILD_DIR, FMI_HEADERS_DIR, REPO_ROOT, ensure_directory, ensure_parent_dir
from scripts.generation.generate_c_interface_defs import common_header_name, generate_headers, part_header_name
from scripts.utils.c_interface_export import output_indexes, part_variable_specs
from scripts.utils.sysml_helpers import load_architecture

NATIVE_ROOT = REPO_ROOT / "native" / "flightgear_bridge"
DEFAULT_OUTPUT = BUILD_DIR / "fmus" / "Aircraft_FlightGearBridge.fmu"
DEFAULT_BUILD_DIR = BUILD_DIR / "native" / "flightgear_bridge"
MODEL_IDENTIFIER = "FlightGearBridge"
MODEL_GUID = "{2d7d0b06-4525-4e59-b188-2a9b0b8cb5bb}"
GENERATED_INTERFACE_DIR = REPO_ROOT / "generated" / "interfaces"
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


def _add_scalar(parent: ET.Element, *, name: str, value_reference: int, causality: str, fmi_type: str, variability: str | None = None, start: str | None = None) -> None:
    attrib = {"name": name, "valueReference": str(value_reference), "causality": causality}
    if variability:
        attrib["variability"] = variability
    scalar = ET.SubElement(parent, "ScalarVariable", attrib=attrib)
    value_elem = ET.SubElement(scalar, fmi_type)
    if start is not None:
        value_elem.set("start", start)


def _build_model_description(output_path: Path) -> None:
    architecture = load_architecture(REPO_ROOT / "architecture")
    part = architecture.parts[MODEL_IDENTIFIER]
    specs = part_variable_specs(part)

    root = ET.Element(
        "fmiModelDescription",
        attrib={
            "fmiVersion": "2.0",
            "modelName": "Aircraft.FlightGearBridge",
            "guid": MODEL_GUID,
            "description": "Native FlightGear generic-protocol bridge FMU",
            "version": "1.0",
            "generationTool": "test_flight_simulator native FMU tooling",
            "generationDateAndTime": "2026-03-27T00:00:00Z",
            "variableNamingConvention": "structured",
            "numberOfEventIndicators": "0",
        },
    )
    co_sim = ET.SubElement(
        root,
        "CoSimulation",
        attrib={
            "modelIdentifier": MODEL_IDENTIFIER,
            "needsExecutionTool": "false",
            "canHandleVariableCommunicationStepSize": "true",
            "canInterpolateInputs": "false",
            "maxOutputDerivativeOrder": "0",
            "canRunAsynchronuously": "false",
            "canBeInstantiatedOnlyOncePerProcess": "false",
            "canNotUseMemoryManagementFunctions": "true",
            "canGetAndSetFMUstate": "false",
            "canSerializeFMUstate": "false",
            "providesDirectionalDerivative": "false",
        },
    )
    source_files = ET.SubElement(co_sim, "SourceFiles")
    for path in FLIGHTGEAR_BRIDGE_PROJECT.staged_files:
        ET.SubElement(source_files, "File", attrib={"name": path.name})

    model_variables = ET.SubElement(root, "ModelVariables")
    for spec in specs:
        _add_scalar(
            model_variables,
            name=spec.name,
            value_reference=spec.value_reference,
            causality=spec.causality,
            fmi_type=spec.fmi_type,
            variability=spec.variability,
            start=spec.start_value,
        )

    model_structure = ET.SubElement(root, "ModelStructure")
    outputs_elem = ET.SubElement(model_structure, "Outputs")
    initial_unknowns = ET.SubElement(model_structure, "InitialUnknowns")
    for idx in output_indexes(specs):
        ET.SubElement(outputs_elem, "Unknown", attrib={"index": str(idx)})
        ET.SubElement(initial_unknowns, "Unknown", attrib={"index": str(idx)})

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    ensure_parent_dir(output_path)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


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

    if build_dir.exists():
        shutil.rmtree(build_dir)
    ensure_directory(build_dir)
    ensure_directory(binary_dir)
    ensure_directory(source_dir)

    built_lib = _build_native_library(FLIGHTGEAR_BRIDGE_PROJECT, build_dir)

    shutil.copy2(built_lib, binary_dir / f"{MODEL_IDENTIFIER}.so")
    for path in FLIGHTGEAR_BRIDGE_PROJECT.staged_files:
        shutil.copy2(path, source_dir / path.name)
    _build_model_description(stage_dir / "modelDescription.xml")

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
