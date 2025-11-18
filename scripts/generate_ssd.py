#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import xml.etree.ElementTree as ET

from utils.sysmlv2_arch_parser import SysMLArchitecture, SysMLAttribute, SysMLPortDefinition, SysMLPortEndpoint, parse_sysml_folder

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCH_PATH = REPO_ROOT / "architecture"
BUILD_DIR = REPO_ROOT / "generated"

SSD_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureDescription"
SSC_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureCommon"
SSV_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureParameterValues"
SSM_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureParameterMapping"
SSB_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureSignalDictionary"



ET.register_namespace("ssd", SSD_NAMESPACE)
ET.register_namespace("ssc", SSC_NAMESPACE)
ET.register_namespace("ssv", SSV_NAMESPACE)
ET.register_namespace("ssm", SSM_NAMESPACE)
ET.register_namespace("ssb", SSB_NAMESPACE)

PRIMITIVE_TYPE_MAP = {
    "real": "Real",
    "float": "Real",
    "float32": "Real",
    "double": "Real",
    "integer": "Integer",
    "int": "Integer",
    "int8": "Integer",
    "uint8": "Integer",
    "boolean": "Boolean",
    "bool": "Boolean",
    "string": "String",
}

MODEL_CLASS_MAP: Dict[str, str] = {
    "CompositeAirframe": "Aircraft.CompositeAirframe",
    "TurbofanPropulsion": "Aircraft.TurbofanPropulsion",
    "AdaptiveWingSystem": "Aircraft.AdaptiveWingSystem",
    "MissionComputer": "Aircraft.MissionComputer",
    "AutopilotModule": "Aircraft.AutopilotModule",
    "InputOutput": "Aircraft.InputOutput",
    "FuelSystem": "Aircraft.FuelSystem",
    "ControlInterface": "Aircraft.ControlInterface",
    "Environment": "Aircraft.Environment",
}


def fmu_source(component_name: str) -> str:
    modelica_class = MODEL_CLASS_MAP.get(component_name)
    if not modelica_class:
        raise KeyError(f"No Modelica class map defined for component '{component_name}'")
    fmu_filename = modelica_class.replace(".", "_") + ".fmu"
    return f"resources/{fmu_filename}"


def _primitive_type(type_name: Optional[str]) -> str:
    if not type_name:
        return "Real"
    key = type_name.strip().lower()
    return PRIMITIVE_TYPE_MAP.get(key, "Real")


def _unique_component_name(name: str, used: Dict[str, str]) -> str:
    base = "".join(ch if ch.isalnum() else "_" for ch in name).strip("_") or "Component"
    candidate = base
    suffix = 2
    while candidate in used.values():
        candidate = f"{base}{suffix}"
        suffix += 1
    return candidate


def _expand_payload_definition(
    payload_def: Optional[SysMLPortDefinition],
    definitions: Dict[str, SysMLPortDefinition],
    visited: Optional[Tuple[str, ...]] = None,
) -> List[Tuple[str, str]]:
    if payload_def is None:
        return [("", "Real")]
    visited = tuple(visited or ())
    if payload_def.name in visited:
        return [("", "Real")]

    entries: List[Tuple[str, str]] = []
    for attr in payload_def.attributes.values():
        attr_type = attr.type or ""
        if attr_type in definitions:
            nested = definitions[attr_type]
            for suffix, primitive in _expand_payload_definition(
                nested, definitions, visited + (payload_def.name,)
            ):
                field_name = attr.name if not suffix else f"{attr.name}.{suffix}"
                entries.append((field_name, primitive))
        else:
            entries.append((attr.name, _primitive_type(attr.type)))
    if not entries:
        entries.append(("", "Real"))
    return entries


def _expand_port_entries(
    port: SysMLPortEndpoint, architecture: SysMLArchitecture
) -> List[Dict[str, str]]:
    if port.direction not in {"in", "out"}:
        return []
    kind = "input" if port.direction == "in" else "output"
    payload_entries = _expand_payload_definition(port.payload_def, architecture.port_definitions)
    results: List[Dict[str, str]] = []
    for suffix, primitive in payload_entries:
        connector_name = port.name if not suffix else f"{port.name}.{suffix}"
        results.append(
            {
                "connector_name": connector_name,
                "kind": kind,
                "primitive": primitive,
                "suffix": suffix,
            }
        )
    return results


def _parse_literal(value: Optional[str]):
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        pass
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        if any(ch in text for ch in (".", "e", "E")):
            return float(text)
        return int(text)
    except ValueError:
        return text


def _infer_primitive(attr: SysMLAttribute, sample) -> str:
    if attr.type:
        return _primitive_type(attr.type)
    if isinstance(sample, bool):
        return "Boolean"
    if isinstance(sample, int):
        return "Integer"
    if isinstance(sample, float):
        return "Real"
    if isinstance(sample, str):
        return "String"
    return "Real"


def _parameter_connector_entries(attributes: Dict[str, SysMLAttribute]) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for name in sorted(attributes):
        attr = attributes[name]
        literal = _parse_literal(attr.value)
        if isinstance(literal, (list, tuple)):
            sample = next((item for item in literal if item is not None), None)
            primitive = _infer_primitive(attr, sample)
            if literal:
                for idx, _ in enumerate(literal, start=1):
                    entries.append(
                        {"connector_name": f"{attr.name}[{idx}]", "primitive": primitive}
                    )
            else:
                entries.append({"connector_name": attr.name, "primitive": primitive})
            continue

        primitive = _infer_primitive(attr, literal)
        entries.append({"connector_name": attr.name, "primitive": primitive})
    return entries


def build_ssd_tree(architecture: SysMLArchitecture) -> ET.ElementTree:
    system_name = architecture.package
    components = [(name, part) for name, part in architecture.parts.items() if name != "Aircraft"]
    component_names: Dict[str, str] = {}
    connector_lookup: Dict[str, Dict[str, Dict[str, str]]] = {}

    root = ET.Element(
        f"{{{SSD_NAMESPACE}}}SystemStructureDescription",
        attrib={
            "name": system_name,
            "version": "1.0",
        },
    )

    system_elem = ET.SubElement(root, f"{{{SSD_NAMESPACE}}}System", attrib={"name": system_name})
    elements_elem = ET.SubElement(system_elem, f"{{{SSD_NAMESPACE}}}Elements")

    for part_name, part in components:
        component_names[part_name] = _unique_component_name(part_name, component_names)
        display_name = component_names[part_name]
        component_elem = ET.SubElement(
            elements_elem,
            f"{{{SSD_NAMESPACE}}}Component",
            attrib={
                "name": display_name,
                "type": "application/x-fmu-sharedlibrary",
                "source": fmu_source(part_name),
            },
        )
        connector_entries: List[Dict[str, str]] = []
        port_map: Dict[str, Dict[str, str]] = {}
        for port in part.ports:
            entries = _expand_port_entries(port, architecture)
            if not entries:
                continue
            port_map[port.name] = {
                entry["suffix"]: entry["connector_name"] for entry in entries
            }
            connector_entries.extend(entries)

        parameter_entries = _parameter_connector_entries(part.attributes)

        if connector_entries or parameter_entries:
            connectors_elem = ET.SubElement(component_elem, f"{{{SSD_NAMESPACE}}}Connectors")
            for entry in connector_entries:
                connector_elem = ET.SubElement(
                    connectors_elem,
                    f"{{{SSD_NAMESPACE}}}Connector",
                    attrib={"name": entry["connector_name"], "kind": entry["kind"]},
                )
                ET.SubElement(connector_elem, f"{{{SSC_NAMESPACE}}}{entry['primitive']}")
            for param in parameter_entries:
                connector_elem = ET.SubElement(
                    connectors_elem,
                    f"{{{SSD_NAMESPACE}}}Connector",
                    attrib={"name": param["connector_name"], "kind": "parameter"},
                )
                ET.SubElement(connector_elem, f"{{{SSC_NAMESPACE}}}{param['primitive']}")

        connector_lookup[part_name] = port_map

    connections_elem = ET.SubElement(system_elem, f"{{{SSD_NAMESPACE}}}Connections")
    for conn in architecture.connections:
        start_component = component_names.get(conn.src_component)
        end_component = component_names.get(conn.dst_component)
        if not start_component or not end_component:
            continue
        start_variants = connector_lookup.get(conn.src_component, {}).get(conn.src_port)
        end_variants = connector_lookup.get(conn.dst_component, {}).get(conn.dst_port)
        if not start_variants or not end_variants:
            continue
        for suffix, start_connector in start_variants.items():
            end_connector = end_variants.get(suffix)
            if not end_connector:
                continue
            ET.SubElement(
                connections_elem,
                f"{{{SSD_NAMESPACE}}}Connection",
                attrib={
                    "startElement": start_component,
                    "startConnector": start_connector,
                    "endElement": end_component,
                    "endConnector": end_connector,
                },
            )

    ET.SubElement(
        root,
        f"{{{SSD_NAMESPACE}}}DefaultExperiment",
        attrib={"startTime": "0", "stopTime": "3600"},
    )

    return ET.ElementTree(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=ARCH_PATH,
        help="Directory containing the SysML architecture (.sysml) files or a file within it.",
    )
    parser.add_argument("--output", type=Path, default=BUILD_DIR / "SystemStructure.ssd")

    args = parser.parse_args()

    source = args.architecture
    if source.is_file():
        source = source.parent
    args.output.parent.mkdir(parents=True, exist_ok=True) 

    architecture = parse_sysml_folder(source)
    tree = build_ssd_tree(architecture)
    ET.indent(tree, space="  ", level=0)
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    print(f"SSD written to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        raise
