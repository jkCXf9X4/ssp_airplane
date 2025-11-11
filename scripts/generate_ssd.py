#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Tuple

import xml.etree.ElementTree as ET
# from xml.dom import minidom

from sysml_loader import MODEL_CLASS_MAP, load_architecture

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCH_PATH = REPO_ROOT / "architecture" / "aircraft_architecture.sysml"
BUILD_DIR = REPO_ROOT / "build" / "structure"
SSD_NAMESPACE = "http://www.fmi-standard.org/SSP1/SystemStructureDescription"
ET.register_namespace("ssd", SSD_NAMESPACE)


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
    return f"fmus/{fmu_filename}"


def build_ssd_tree(data: dict, destination: Path) -> ET.ElementTree:
    system_name = data["metadata"]["system"]
    components = [c for c in data["components"] if c["id"] != "comp.airframe"]
    id_to_name = component_name_map(components)

    root = ET.Element(f"{{{SSD_NAMESPACE}}}SystemStructureDescription", attrib={
        "name": system_name,
        "version": "1.0",
    })

    default_exp = ET.SubElement(root, f"{{{SSD_NAMESPACE}}}DefaultExperiment", attrib={
        "startTime": "0",
        "stopTime": "3600",
    })

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
        connectors_elem = ET.SubElement(component_elem, f"{{{SSD_NAMESPACE}}}Connectors")
        for port in comp.get("ports", []):
            ET.SubElement(
                connectors_elem,
                f"{{{SSD_NAMESPACE}}}Connector",
                attrib={
                    "name": port["name"],
                    "kind": port.get("kind", "data"),
                    "type": "Real",
                },
            )

    connections_elem = ET.SubElement(system_elem, f"{{{SSD_NAMESPACE}}}Connections")
    for conn in data.get("connectors", []):
        start_comp_id, start_port = split_endpoint(conn["from"])
        end_comp_id, end_port = split_endpoint(conn["to"])
        start_name = f"{id_to_name[start_comp_id]}.{start_port}"
        end_name = f"{id_to_name[end_comp_id]}.{end_port}"
        ET.SubElement(
            connections_elem,
            f"{{{SSD_NAMESPACE}}}Connection",
            attrib={
                "startElement": start_name,
                "endElement": end_name,
            },
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
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tree = build_ssd_tree(data, args.output)
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    print(f"SSD written to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        raise
