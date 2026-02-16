#!/usr/bin/env python3
"""Generate FMI 2.0 `modelDescription.xml` stubs for every component in the SysML architecture."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import sys
from pathlib import Path
from typing import Iterable, Optional
from uuid import NAMESPACE_URL, uuid5
import xml.etree.ElementTree as ET
import zipfile

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import (
    ARCHITECTURE_DIR,
    BUILD_DIR,
    GENERATED_DIR,
    DEFAULT_MODELS,
    ensure_directory,
)

from scripts.utils.fmi_helpers import format_start_value, map_fmi_type

from pycps_sysmlv2 import (
    SysMLArchitecture,
    SysMLPartDefinition,
    load_architecture,
)

from scripts.utils.sysml_compat import (
    architecture_package,
    composition_components,
    literal_value,
    part_ports,
)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT_DIR = GENERATED_DIR / "model_descriptions"

CO_SIMULATION_ATTRS = {
    "modelIdentifier": "",
}


@dataclass
class VariableSpec:
    name: str
    causality: str
    value_reference: int
    index: int
    fmi_type: str
    variability: Optional[str] = None
    description: Optional[str] = None
    start_value: Optional[str] = None


def _port_attribute_variables(
    part: SysMLPartDefinition, starting_ref: int, starting_index: int
) -> tuple[list[VariableSpec], int, list[int]]:
    print("Parsing ports")

    variables: list[VariableSpec] = []
    value_ref = starting_ref
    value_index = starting_index

    for port in part.ports.values():
        port_def = port.payload_def
        attributes = port_def.attributes.values()

        if not attributes:
            print(f"WARNING: The port {port.name} does not have any attributes")
            continue

        for attr in attributes:
            var_name = f"{port.name}.{attr.name}"
            fmi_type = attr.type
            description = attr.doc or port.doc or (port_def.doc if port_def else None)
            spec = VariableSpec(
                name=var_name,
                causality="input" if port.direction == "in" else "output",
                value_reference=value_ref,
                fmi_type=fmi_type,
                description=description,
                index=value_index,
            )
            variables.append(spec)
            value_ref += 1
            value_index += 1

    return variables, value_ref, value_index


def _parameter_variables(
    part: SysMLPartDefinition, starting_ref: int, starting_index: int
) -> tuple[list[VariableSpec], int]:
    
    print("Parsing parameters")

    variables: list[VariableSpec] = []
    value_ref = starting_ref
    value_index = starting_index

    for attr_name, attr in part.attributes.items():
        print(f"Parsing {attr_name}, {attr.type}")
        literal = attr.value

        if isinstance(literal, (list, tuple)):
            print("List")
            if not literal:
                print(
                    f"Unable to infer fmi type from attribute, {part.name}.{attr_name}"
                )
                continue

            fmi_type = map_fmi_type("Real")

            for idx, item in enumerate(literal, start=0):
                spec = VariableSpec(
                    name=f"{attr.name}[{idx}]",
                    causality="parameter",
                    value_reference=value_ref,
                    fmi_type=fmi_type,
                    variability="fixed",
                    description=attr.doc,
                    start_value=format_start_value(fmi_type, item),
                    index=value_index,
                )
                variables.append(spec)
                value_ref += 1
                value_index += 1

        else:
            print("Not list")
            fmi_type = map_fmi_type(attr.type)

            spec = VariableSpec(
                name=attr.name,
                causality="parameter",
                value_reference=value_ref,
                fmi_type=fmi_type,
                variability="fixed",
                description=attr.doc,
                start_value=format_start_value(fmi_type, literal),
                index=value_index,
            )
            variables.append(spec)
            value_ref += 1
            value_index += 1

    return variables, value_ref, value_index


def _get_variables(part: SysMLPartDefinition):
    print("Parsing variables")
    value_ref = 0
    index = 1

    parameter_vars, value_ref, index = _parameter_variables(part, value_ref, index)
    port_vars, value_ref, index = _port_attribute_variables(part, value_ref, index)

    return parameter_vars + port_vars


def _write_scalar_variable(parent: ET.Element, spec: VariableSpec) -> None:
    attrib = {
        "name": spec.name,
        "valueReference": str(spec.value_reference),
    }
    if spec.causality:
        attrib["causality"] = spec.causality
    if spec.variability:
        attrib["variability"] = spec.variability
    if spec.description:
        attrib["description"] = spec.description
    scalar = ET.SubElement(parent, "ScalarVariable", attrib=attrib)
    data_type = ET.SubElement(scalar, spec.fmi_type)
    if spec.start_value is not None:
        data_type.set("start", spec.start_value)


def _build_model_description_tree(
    part: SysMLPartDefinition, package_name: str
) -> ET.ElementTree:
    timestamp = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    guid = str(uuid5(NAMESPACE_URL, f"ssp_airplane/{package_name}/{part.name}"))

    root = ET.Element(
        "fmiModelDescription",
        attrib={
            "fmiVersion": "2.0",
            "modelName": f"{package_name}.{part.name}",
            "guid": f"{{{guid}}}",
            "description": part.doc or "",
            "version": "1.0",
            "generationTool": "ssp_airplane tooling",
            "generationDateAndTime": timestamp,
            "variableNamingConvention": "structured",
            "numberOfEventIndicators": "0",
        },
    )

    co_sim_attrs = dict(CO_SIMULATION_ATTRS)
    co_sim_attrs["modelIdentifier"] = part.name
    ET.SubElement(root, "CoSimulation", attrib=co_sim_attrs)

    model_vars = ET.SubElement(root, "ModelVariables")

    variables = _get_variables(part)

    for spec in variables:
        _write_scalar_variable(model_vars, spec)

    model_structure = ET.SubElement(root, "ModelStructure")
    outputs_elem = ET.SubElement(model_structure, "Outputs")
    initial_elem = ET.SubElement(model_structure, "InitialUnknowns")

    for v in [x for x in variables if x.causality == "output"]:
        ET.SubElement(outputs_elem, "Unknown", attrib={"index": str(v.index)})
        ET.SubElement(initial_elem, "Unknown", attrib={"index": str(v.index)})

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    return tree


def generate_model_descriptions(
    architecture_path: Path,
    output_dir: Path,
    components: Optional[Iterable[str]] = None,
) -> list[Path]:
    ensure_directory(output_dir)

    architecture = load_architecture(architecture_path)
    targets = [x for x in architecture.part_definitions.values() if x.name in components]

    written: list[Path] = []
    for part in targets:
        print(f"Generating MD for {part.name}")

        component_dir = output_dir / part.name
        output_path = component_dir / "modelDescription.xml"
        fmu_dir = BUILD_DIR / "fmu_pre"

        ensure_directory(component_dir)
        ensure_directory(fmu_dir)

        tree = _build_model_description_tree(part, architecture.package)

        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        written.append(output_path)

    return written


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Path to the SysML architecture directory or a file within it.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory that will contain one sub-folder per component, each with a modelDescription.xml.",
    )
    parser.add_argument(
        "--components",
        nargs="*",
        default=DEFAULT_MODELS,
        help="Optional subset of component instance/definition names to generate.",
    )
    args = parser.parse_args(argv)

    try:
        written = generate_model_descriptions(
            args.architecture, args.output_dir, args.components
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    if not written:
        print("No components matched the provided criteria.")
        return 1
    for path in written:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
