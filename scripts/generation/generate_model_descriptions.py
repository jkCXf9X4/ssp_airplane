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

from scripts.common.paths import ARCHITECTURE_DIR, BUILD_DIR, GENERATED_DIR
from sysml.values import parse_literal
from sysml.helpers import load_architecture
from sysml.parser import (
    SysMLArchitecture,
    SysMLAttribute,
    SysMLPartDefinition,
)
from sysml.type_utils import infer_primitive, normalize_primitive, optional_primitive

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
    fmi_type: str
    variability: Optional[str] = None
    description: Optional[str] = None
    start_value: Optional[str] = None


def _format_start_value(fmi_type: str, literal: Optional[object]) -> Optional[str]:
    if literal is None:
        return None
    if fmi_type == "Real":
        return f"{float(literal):g}"
    if fmi_type == "Integer":
        return str(int(literal))
    if fmi_type == "Boolean":
        return "true" if bool(literal) else "false"
    if fmi_type == "String":
        return str(literal)
    return None


def _port_attribute_variables(part: SysMLPartDefinition, starting_ref: int) -> tuple[list[VariableSpec], int, list[int]]:
    variables: list[VariableSpec] = []
    output_indexes: list[int] = []
    value_ref = starting_ref
    for port in sorted(part.ports, key=lambda item: item.name):
        payload_def = port.payload_def
        attributes = (
            [payload_def.attributes[name] for name in sorted(payload_def.attributes)]
            if payload_def
            else []
        )
        if not attributes:
            spec = VariableSpec(
                name=port.name,
                causality="input" if port.direction == "in" else "output",
                value_reference=value_ref,
                fmi_type="Real",
                description=port.doc,
            )
            variables.append(spec)
            if port.direction == "out":
                output_indexes.append(value_ref)
            value_ref += 1
            continue

        for attr in attributes:
            var_name = f"{port.name}.{attr.name}"
            literal = parse_literal(attr.value)
            fmi_type = optional_primitive(attr.type) or "Real"
            description = attr.doc or port.doc or (payload_def.doc if payload_def else None)
            spec = VariableSpec(
                name=var_name,
                causality="input" if port.direction == "in" else "output",
                value_reference=value_ref,
                fmi_type=fmi_type,
                description=description,
            )
            variables.append(spec)
            if port.direction == "out":
                output_indexes.append(value_ref)
            value_ref += 1
    return variables, value_ref, output_indexes


def _parameter_variables(part: SysMLPartDefinition, starting_ref: int) -> tuple[list[VariableSpec], int]:
    variables: list[VariableSpec] = []
    value_ref = starting_ref
    for attr_name in sorted(part.attributes):
        attr = part.attributes[attr_name]
        literal = parse_literal(attr.value)
        fmi_type = infer_primitive(attr.type, literal)
        spec = VariableSpec(
            name=attr.name,
            causality="parameter",
            value_reference=value_ref,
            fmi_type=fmi_type,
            variability="fixed",
            description=attr.doc,
            start_value=_format_start_value(fmi_type, literal),
        )
        variables.append(spec)
        value_ref += 1
    return variables, value_ref


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


def _build_model_description_tree(part: SysMLPartDefinition, architecture: SysMLArchitecture) -> ET.ElementTree:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    guid = str(uuid5(NAMESPACE_URL, f"ssp_airplane/{architecture.package}/{part.name}"))

    root = ET.Element(
        "fmiModelDescription",
        attrib={
            "fmiVersion": "2.0",
            "modelName": f"{architecture.package}.{part.name}",
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
    value_ref = 1
    port_vars, value_ref, output_indexes = _port_attribute_variables(part, value_ref)
    parameter_vars, value_ref = _parameter_variables(part, value_ref)

    for spec in port_vars + parameter_vars:
        _write_scalar_variable(model_vars, spec)

    model_structure = ET.SubElement(root, "ModelStructure")
    if output_indexes:
        outputs_elem = ET.SubElement(model_structure, "Outputs")
        initial_elem = ET.SubElement(model_structure, "InitialUnknowns")
        for idx in output_indexes:
            ET.SubElement(outputs_elem, "Unknown", attrib={"index": str(idx)})
            ET.SubElement(initial_elem, "Unknown", attrib={"index": str(idx)})

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    return tree


def _component_targets(architecture: SysMLArchitecture, include: Optional[Iterable[str]]) -> list[SysMLPartDefinition]:
    if include:
        ordered: list[SysMLPartDefinition] = []
        seen: set[str] = set()
        for name in include:
            name = name.strip()
            if not name or name in seen or name not in architecture.parts:
                continue
            ordered.append(architecture.parts[name])
            seen.add(name)
        return ordered
    return [architecture.parts[name] for name in sorted(architecture.parts)]


def generate_model_descriptions(
    architecture_path: Path,
    output_dir: Path,
    components: Optional[Iterable[str]] = None,
) -> list[Path]:
    architecture = load_architecture(architecture_path)
    targets = _component_targets(architecture, components)
    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for part in targets:
        tree = _build_model_description_tree(part, architecture)
        component_dir = output_dir / part.name
        component_dir.mkdir(parents=True, exist_ok=True)
        output_path = component_dir / "modelDescription.xml"
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        written.append(output_path)
        fmu_dir = BUILD_DIR / "fmu_pre"
        fmu_dir.mkdir(parents=True, exist_ok=True)
        zipfile.ZipFile(fmu_dir /f"{part.name}.fmu", mode='w').write(output_path.as_posix(), arcname="modelDescription.xml")
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
        help="Optional subset of component names to generate (defaults to all parts).",
    )
    args = parser.parse_args(argv)

    try:
        written = generate_model_descriptions(args.architecture, args.output_dir, args.components)
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
