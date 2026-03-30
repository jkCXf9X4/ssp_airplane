#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import (
    COMPOSITION_NAME,
    ARCHITECTURE_DIR,
    GENERATED_DIR,
    ensure_parent_dir,
)
from scripts.common.fmi_helpers import fmu_resource_path, to_fmi_direction_definition
from scripts.common.sysml_values import parse_literal
from scripts.utils.fmi_helpers import architecture_model_map, component_fmu_source
from scripts.utils.type_utils import infer_primitive, normalize_primitive

from pyssp_standard.common_content_ssc import (
    TypeBoolean,
    TypeInteger,
    TypeReal,
    TypeString,
)
from pyssp_standard.ssd import (
    Component,
    Connection,
    Connector,
    DefaultExperiment,
    SSD,
    System,
)
from pycps_sysmlv2 import SysMLPartDefinition, load_system

import logging
logging.basicConfig(level=logging.WARNING)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "SystemStructure.ssd"
SSD_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureDescription"
SSC_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureCommon"


def _type_from_primitive(type: str):
    if type == "Real":
        return TypeReal(unit=None)
    if type == "Integer":
        return TypeInteger()
    if type == "Boolean":
        return TypeBoolean()
    if type == "String":
        return TypeString()
    return TypeReal(unit=None)


def _unique_component_name(name: str, used: Dict[str, str]) -> str:
    base = "".join(ch if ch.isalnum() else "_" for ch in name).strip("_") or "Component"
    candidate = base
    suffix = 2
    while candidate in used.values():
        candidate = f"{base}{suffix}"
        suffix += 1
    return candidate


def _expand_payload_definition(payload_def, definitions: Dict[str, object], visited: Optional[Tuple[str, ...]] = None) -> List[Tuple[str, str]]:
    if payload_def is None:
        return [("", "Real")]
    visited = tuple(visited or ())
    if payload_def.name in visited:
        return [("", "Real")]

    entries: List[Tuple[str, str]] = []
    for attr in payload_def.attributes.values():
        attr_type = getattr(attr.type, "as_string", lambda: attr.type)() or ""
        if attr_type in definitions:
            nested = definitions[attr_type]
            for suffix, primitive in _expand_payload_definition(
                nested, definitions, visited + (payload_def.name,)
            ):
                field_name = attr.name if not suffix else f"{attr.name}.{suffix}"
                entries.append((field_name, primitive))
        else:
            entries.append((attr.name, normalize_primitive(attr_type)))
    if not entries:
        entries.append(("", "Real"))
    return entries


def _expand_port_entries(port, architecture) -> List[Dict[str, str]]:
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


def _parameter_connector_entries(attributes: Dict[str, object]) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for name in sorted(attributes):
        attr = attributes[name]
        literal = parse_literal(getattr(attr, "value", None))
        if literal is None:
            literal = getattr(attr, "value", None)
        if isinstance(literal, (list, tuple)):
            sample = next((item for item in literal if item is not None), None)
            primitive = infer_primitive(getattr(attr, "type", None), sample)
            if literal:
                for idx, _ in enumerate(literal, start=1):
                    entries.append(
                        {"connector_name": f"{attr.name}[{idx}]", "primitive": primitive}
                    )
            else:
                entries.append({"connector_name": attr.name, "primitive": primitive})
            continue

        type_name = getattr(attr.type, "as_string", lambda: attr.type)()
        primitive = infer_primitive(type_name, literal)
        entries.append({"connector_name": attr.name, "primitive": primitive})
    return entries


def build_ssd_tree(architecture, class_map: Optional[Dict[str, str]] = None) -> ET.ElementTree:
    class_map = class_map or architecture_model_map(architecture)
    system_name = architecture.package
    components = list(architecture.parts.items())
    component_names: Dict[str, str] = {}
    connector_lookup: Dict[str, Dict[str, Dict[str, str]]] = {}

    root = ET.Element(
        f"{{{SSD_NAMESPACE}}}SystemStructureDescription",
        attrib={"name": system_name, "version": "1.0"},
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
    for conn in getattr(architecture, "connections", []):
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


def build_ssd(ssd: SSD, system: SysMLPartDefinition) -> None:

    logging.info(f"Building system: {system.name}")
    ssd.name = system.name
    ssd.version = "1.0"
    ssd.system = System(name=system.name)

    logging.info("Adding connectors")
    for part_name, part_ref in system.parts.items():
        part = part_ref.part_def
        logging.debug(f"Processing part: {part_name}")
        component = Component()
        component.name = part_name
        component.component_type = "application/x-fmu-sharedlibrary"
        component.source = fmu_resource_path(part.name)

        for port_ref, port_def, attribute in part.get_port_attributes():
            logging.debug(f"Parsing port {port_ref.name}")
            name = port_ref.name + "." + attribute.name
            c = Connector(
                name=name,
                kind=to_fmi_direction_definition(port_ref.direction),
                type_=_type_from_primitive(attribute.type.as_string()),
            )
            component.connectors.append(c)

        for attrib_name, attribute in part.attributes.items():
            logging.debug(f"Parsing parameter {attrib_name}")

            for idx, _ in attribute.enumerator():
                if attribute.is_list():
                    name = f"{attrib_name}[{idx}]"
                else:
                    name = attrib_name

                c = Connector(
                    name=name,
                    kind="parameter",
                    type_=_type_from_primitive(attribute.type.as_string()),
                )
                component.connectors.append(c)

        ssd.system.elements.append(component)

    logging.info("Adding connections")
    for conn in system.connections:
        if conn.src_port_def is not conn.dst_port_def:
            raise Exception(
                f"Src {conn.src_port_def.name} and dest port {conn.dst_port_def.name} must be same type"
            )

        logging.debug(
            f"Processing connection: {conn.src_component}.{conn.src_port} -> {conn.dst_component}.{conn.dst_port}"
        )

        if conn.src_port_def is None:
            raise Exception("Port definition not connected")
        port = conn.src_port_def

        for attribute_name, attribute in port.attributes.items():
            c = Connection(
                start_element=conn.src_component,
                start_connector=conn.src_port + "." + attribute_name,
                end_element=conn.dst_component,
                end_connector=conn.dst_port + "." + attribute_name,
            )
            ssd.add_connection(c)

    logging.info("Adding default experiment")
    default_experiment = DefaultExperiment()
    default_experiment.start_time = 0
    default_experiment.stop_time = 3600
    ssd.default_experiment = default_experiment

    logging.info("System ssd is completed")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Directory containing the SysML architecture (.sysml) files or a file within it.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )
    parser.add_argument(
        "--composition",
        default=COMPOSITION_NAME,
        help="Optional subset of component instance/definition names to generate.",
    )

    args = parser.parse_args(argv)

    try:
        logging.info(f"[generate_ssd] args:{vars(args)}")
        system = load_system(args.architecture, args.composition)
        ensure_parent_dir(args.output)
        with SSD(args.output, mode="w") as ssd:
            build_ssd(ssd, system)

    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(f"SSD written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
