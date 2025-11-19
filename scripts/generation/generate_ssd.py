#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import xml.etree.ElementTree as ET

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR
from scripts.common.sysml_values import parse_literal
from scripts.utils.fmi_helpers import architecture_model_map, component_fmu_source
from scripts.utils.sysml_helpers import load_architecture
from scripts.utils.sysmlv2_arch_parser import (
    SysMLArchitecture,
    SysMLAttribute,
    SysMLPortDefinition,
    SysMLPortEndpoint,
)
from scripts.utils.ssp_helpers import (
    SSD_NAMESPACE,
    SSC_NAMESPACE,
    SSV_NAMESPACE,
    SSM_NAMESPACE,
    SSB_NAMESPACE,
    register_ssp_namespaces,
)
from scripts.utils.type_utils import infer_primitive, normalize_primitive

register_ssp_namespaces()

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
BUILD_DIR = GENERATED_DIR

def _primitive_type(type_name: Optional[str]) -> str:
    return normalize_primitive(type_name)


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


def _parameter_connector_entries(attributes: Dict[str, SysMLAttribute]) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for name in sorted(attributes):
        attr = attributes[name]
        literal = parse_literal(attr.value)
        if isinstance(literal, (list, tuple)):
            sample = next((item for item in literal if item is not None), None)
            primitive = infer_primitive(attr.type, sample)
            if literal:
                for idx, _ in enumerate(literal, start=1):
                    entries.append(
                        {"connector_name": f"{attr.name}[{idx}]", "primitive": primitive}
                    )
            else:
                entries.append({"connector_name": attr.name, "primitive": primitive})
            continue

        primitive = infer_primitive(attr.type, literal)
        entries.append({"connector_name": attr.name, "primitive": primitive})
    return entries


def build_ssd_tree(
    architecture: SysMLArchitecture, class_map: Optional[Dict[str, str]] = None
) -> ET.ElementTree:
    class_map = class_map or architecture_model_map(architecture)
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
                "source": component_fmu_source(part_name, class_map),
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
        default=DEFAULT_ARCH_PATH,
        help="Directory containing the SysML architecture (.sysml) files or a file within it.",
    )
    parser.add_argument("--output", type=Path, default=BUILD_DIR / "SystemStructure.ssd")

    args = parser.parse_args()

    architecture = load_architecture(args.architecture)
    args.output.parent.mkdir(parents=True, exist_ok=True)
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
