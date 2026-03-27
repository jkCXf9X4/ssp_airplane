#!/usr/bin/env python3
"""Build native FMUs that are implemented outside OpenModelica."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import BUILD_DIR, REPO_ROOT, ensure_directory, ensure_parent_dir

NATIVE_ROOT = REPO_ROOT / "native" / "flightgear_bridge"
DEFAULT_OUTPUT = BUILD_DIR / "fmus" / "Aircraft_FlightGearBridge.fmu"
DEFAULT_BUILD_DIR = BUILD_DIR / "native" / "flightgear_bridge"
MODEL_IDENTIFIER = "FlightGearBridge"
MODEL_GUID = "{2d7d0b06-4525-4e59-b188-2a9b0b8cb5bb}"


def _add_scalar(parent: ET.Element, *, name: str, value_reference: int, causality: str, fmi_type: str, variability: str | None = None, start: str | None = None) -> None:
    attrib = {"name": name, "valueReference": str(value_reference), "causality": causality}
    if variability:
        attrib["variability"] = variability
    scalar = ET.SubElement(parent, "ScalarVariable", attrib=attrib)
    value_elem = ET.SubElement(scalar, fmi_type)
    if start is not None:
        value_elem.set("start", start)


def _build_model_description(output_path: Path) -> None:
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
    ET.SubElement(source_files, "File", attrib={"name": "FlightGearBridge.cpp"})
    ET.SubElement(source_files, "File", attrib={"name": "BridgeRuntime.cpp"})
    ET.SubElement(source_files, "File", attrib={"name": "BridgeRuntime.hpp"})

    model_variables = ET.SubElement(root, "ModelVariables")
    output_indexes: list[int] = []

    # Parameters
    _add_scalar(model_variables, name="transport", value_reference=0, causality="parameter", variability="fixed", fmi_type="String", start="FlightGearGeneric")
    _add_scalar(model_variables, name="reference_latitude_deg", value_reference=1, causality="parameter", variability="fixed", fmi_type="Real", start="0")
    _add_scalar(model_variables, name="reference_longitude_deg", value_reference=2, causality="parameter", variability="fixed", fmi_type="Real", start="0")
    _add_scalar(model_variables, name="reference_altitude_m", value_reference=3, causality="parameter", variability="fixed", fmi_type="Real", start="0")
    _add_scalar(model_variables, name="remote_host", value_reference=4, causality="parameter", variability="fixed", fmi_type="String", start="127.0.0.1")
    _add_scalar(model_variables, name="telemetry_port", value_reference=5, causality="parameter", variability="fixed", fmi_type="Integer", start="5501")
    _add_scalar(model_variables, name="control_port", value_reference=6, causality="parameter", variability="fixed", fmi_type="Integer", start="5502")

    # Inputs
    input_specs = [
        ("statePosition.x_km", 10, "Real"),
        ("statePosition.y_km", 11, "Real"),
        ("statePosition.z_km", 12, "Real"),
        ("stateOrientation.roll_deg", 13, "Real"),
        ("stateOrientation.pitch_deg", 14, "Real"),
        ("stateOrientation.yaw_deg", 15, "Real"),
        ("flightStatus.airspeed_mps", 16, "Real"),
        ("flightStatus.energy_state_norm", 17, "Real"),
        ("flightStatus.angle_of_attack_deg", 18, "Real"),
        ("flightStatus.climb_rate", 19, "Real"),
        ("flightStatus.health_code", 20, "Integer"),
        ("missionStatus.waypoint_index", 21, "Integer"),
        ("missionStatus.total_waypoints", 22, "Integer"),
        ("missionStatus.distance_to_waypoint_km", 23, "Real"),
        ("missionStatus.arrived", 24, "Boolean"),
        ("missionStatus.complete", 25, "Boolean"),
    ]
    for name, vr, fmi_type in input_specs:
        _add_scalar(model_variables, name=name, value_reference=vr, causality="input", fmi_type=fmi_type)

    # Outputs
    output_specs = [
        ("pilotCommand.stick_pitch_norm", 40, "Real"),
        ("pilotCommand.stick_roll_norm", 41, "Real"),
        ("pilotCommand.rudder_norm", 42, "Real"),
        ("pilotCommand.throttle_norm", 43, "Real"),
        ("pilotCommand.throttle_aux_norm", 44, "Real"),
        ("pilotCommand.button_mask", 45, "Integer"),
        ("pilotCommand.hat_x", 46, "Integer"),
        ("pilotCommand.hat_y", 47, "Integer"),
        ("pilotCommand.mode_switch", 48, "Integer"),
        ("pilotCommand.reserved", 49, "Integer"),
    ]
    for index, (name, vr, fmi_type) in enumerate(output_specs, start=1):
        _add_scalar(model_variables, name=name, value_reference=vr, causality="output", fmi_type=fmi_type)
        output_indexes.append(len(input_specs) + 7 + index)

    model_structure = ET.SubElement(root, "ModelStructure")
    outputs_elem = ET.SubElement(model_structure, "Outputs")
    initial_unknowns = ET.SubElement(model_structure, "InitialUnknowns")
    for idx in output_indexes:
        ET.SubElement(outputs_elem, "Unknown", attrib={"index": str(idx)})
        ET.SubElement(initial_unknowns, "Unknown", attrib={"index": str(idx)})

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    ensure_parent_dir(output_path)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def build_flightgear_bridge_fmu(output_fmu: Path = DEFAULT_OUTPUT, build_dir: Path = DEFAULT_BUILD_DIR) -> Path:
    stage_dir = build_dir / "stage"
    binary_dir = stage_dir / "binaries" / "linux64"
    source_dir = stage_dir / "sources"

    if build_dir.exists():
        shutil.rmtree(build_dir)
    ensure_directory(build_dir)
    ensure_directory(binary_dir)
    ensure_directory(source_dir)

    subprocess.run(
        ["cmake", "-S", str(NATIVE_ROOT), "-B", str(build_dir), "-DCMAKE_BUILD_TYPE=Release"],
        check=True,
        cwd=REPO_ROOT,
    )
    subprocess.run(
        ["cmake", "--build", str(build_dir), "--config", "Release"],
        check=True,
        cwd=REPO_ROOT,
    )

    built_lib = build_dir / f"{MODEL_IDENTIFIER}.so"
    if not built_lib.exists():
        raise SystemExit(f"Native bridge library not found: {built_lib}")

    shutil.copy2(built_lib, binary_dir / f"{MODEL_IDENTIFIER}.so")
    shutil.copy2(NATIVE_ROOT / "src" / "FlightGearBridge.cpp", source_dir / "FlightGearBridge.cpp")
    shutil.copy2(NATIVE_ROOT / "src" / "BridgeRuntime.cpp", source_dir / "BridgeRuntime.cpp")
    shutil.copy2(NATIVE_ROOT / "src" / "BridgeRuntime.hpp", source_dir / "BridgeRuntime.hpp")
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
