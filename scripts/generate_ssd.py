#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import xml.etree.ElementTree as ET

from sysml_loader import MODEL_CLASS_MAP, load_architecture, get_architecture_text

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCH_PATH = REPO_ROOT / "architecture" / "aircraft_architecture.sysml"
BUILD_DIR = REPO_ROOT / "build" / "structure"
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
}


def split_endpoint(endpoint: str) -> Tuple[str, str]:
    if "." not in endpoint:
        raise ValueError(f"Endpoint '{endpoint}' is missing a port reference")
    comp_id, port = endpoint.rsplit(".", 1)
    return comp_id, port


def component_name_map(components: list[dict]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for comp in components:
        comp_id = comp.get("id")
        if not comp_id:
            continue
        sanitized = comp["name"].replace(" ", "")
        mapping[comp_id] = sanitized
    return mapping


def fmu_source(component_name: str) -> str:
    modelica_class = MODEL_CLASS_MAP.get(component_name)
    if not modelica_class:
        raise KeyError(f"No Modelica class map defined for component '{component_name}'")
    fmu_filename = modelica_class.replace(".", "_") + ".fmu"
    return f"resources/{fmu_filename}"


def parse_data_definitions(text: str) -> Dict[str, List[Tuple[str, str]]]:
    defs: Dict[str, List[Tuple[str, str]]] = {}
    token = "data def"
    idx = 0
    while True:
        start = text.find(token, idx)
        if start == -1:
            break
        brace_start = text.find("{", start)
        if brace_start == -1:
            break
        header = text[start + len(token) : brace_start].strip()
        name = header.split()[0]
        depth = 0
        pos = brace_start
        while pos < len(text):
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
                if depth == 0:
                    block = text[brace_start + 1 : pos]
                    defs[name] = _extract_data_attributes(block)
                    idx = pos + 1
                    break
            pos += 1
        else:
            break
    return defs


def _extract_data_attributes(block: str) -> List[Tuple[str, str]]:
    cleaned = re.sub(r"/\*.*?\*/", "", block, flags=re.S)
    attrs: List[Tuple[str, str]] = []
    for raw_line in cleaned.splitlines():
        line = raw_line.strip()
        if not line.startswith("attribute "):
            continue
        body = line[len("attribute ") :]
        if ":" not in body:
            continue
        name_part, remainder = body.split(":", 1)
        attr_name = name_part.strip()
        type_part = remainder.split(";", 1)[0].strip()
        if attr_name and type_part:
            attrs.append((attr_name, type_part))
    return attrs


def _primitive_type(type_name: Optional[str]) -> str:
    if not type_name:
        return "Real"
    key = type_name.strip().lower()
    return PRIMITIVE_TYPE_MAP.get(key, "Real")


def _expand_type(
    type_name: Optional[str], data_defs: Dict[str, List[Tuple[str, str]]]
) -> List[Tuple[str, str]]:
    if not type_name:
        return [("", "Real")]
    if type_name in data_defs:
        expanded: List[Tuple[str, str]] = []
        for field_name, field_type in data_defs[type_name]:
            for suffix, primitive in _expand_type(field_type, data_defs):
                name = field_name if not suffix else f"{field_name}.{suffix}"
                expanded.append((name, primitive))
        return expanded
    return [("", _primitive_type(type_name))]


def _expand_port_entries(
    port: Dict[str, str], data_defs: Dict[str, List[Tuple[str, str]]]
) -> List[Dict[str, str]]:
    direction = port.get("direction")
    if direction not in {"in", "out"}:
        return []
    kind = "input" if direction == "in" else "output"
    entries: List[Dict[str, str]] = []
    for suffix, primitive in _expand_type(port.get("type"), data_defs):
        connector_name = port["name"] if not suffix else f"{port['name']}.{suffix}"
        entries.append(
            {
                "connector_name": connector_name,
                "kind": kind,
                "primitive": primitive,
                "suffix": suffix,
            }
        )
    if not entries:
        entries.append(
            {"connector_name": port["name"], "kind": kind, "primitive": "Real", "suffix": ""}
        )
    return entries


def build_ssd_tree(data: dict, architecture_text: str, destination: Path) -> ET.ElementTree:
    system_name = data["metadata"]["system"]
    components = [c for c in data["components"] if c["id"] != "comp.airframe"]
    id_to_name = component_name_map(components)
    data_defs = parse_data_definitions(architecture_text)
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

    for comp in components:
        name = id_to_name[comp["id"]]
        component_elem = ET.SubElement(
            elements_elem,
            f"{{{SSD_NAMESPACE}}}Component",
            attrib={
                "name": name,
                "type": "application/x-fmu-sharedlibrary",
                "source": fmu_source(comp["name"]),
            },
        )
        connector_entries: List[Dict[str, str]] = []
        port_map: Dict[str, Dict[str, str]] = {}
        for port in comp.get("ports", []):
            entries = _expand_port_entries(port, data_defs)
            if not entries:
                continue
            port_map[port["name"]] = {
                entry["suffix"]: entry["connector_name"] for entry in entries
            }
            connector_entries.extend(entries)

        if connector_entries:
            connectors_elem = ET.SubElement(component_elem, f"{{{SSD_NAMESPACE}}}Connectors")
            for entry in connector_entries:
                connector_elem = ET.SubElement(
                    connectors_elem,
                    f"{{{SSD_NAMESPACE}}}Connector",
                    attrib={"name": entry["connector_name"], "kind": entry["kind"]},
                )
                ET.SubElement(connector_elem, f"{{{SSC_NAMESPACE}}}{entry['primitive']}")

        connector_lookup[name] = port_map

    connections_elem = ET.SubElement(system_elem, f"{{{SSD_NAMESPACE}}}Connections")
    for conn in data.get("connectors", []):
        start_comp_id, start_port = split_endpoint(conn["from"])
        end_comp_id, end_port = split_endpoint(conn["to"])
        if start_comp_id not in id_to_name or end_comp_id not in id_to_name:
            continue
        start_name = id_to_name[start_comp_id]
        end_name = id_to_name[end_comp_id]
        start_variants = connector_lookup.get(start_name, {}).get(start_port)
        end_variants = connector_lookup.get(end_name, {}).get(end_port)
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
                    "startElement": start_name,
                    "startConnector": start_connector,
                    "endElement": end_name,
                    "endConnector": end_connector,
                },
            )

    ET.SubElement(
        root,
        f"{{{SSD_NAMESPACE}}}DefaultExperiment",
        attrib={"startTime": "0", "stopTime": "3600"},
    )

    return ET.ElementTree(root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=ARCH_PATH)
    parser.add_argument("--output", type=Path, default=BUILD_DIR / "aircraft.ssd")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_architecture(args.architecture)
    architecture_text = get_architecture_text(args.architecture)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tree = build_ssd_tree(data, architecture_text, args.output)
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    print(f"SSD written to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        raise
