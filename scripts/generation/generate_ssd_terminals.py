#!/usr/bin/env python3
"""Generate a compact SSD that relies on FMI terminals for structured connectors."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Optional
import xml.etree.ElementTree as ET

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from scripts.utils.sysmlv2_arch_parser import (
    SysMLArchitecture,
    SysMLPartDefinition,
    parse_sysml_folder,
)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "SystemStructure_terminals.ssd"

SSD_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureDescription"
SSC_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureCommon"
SSV_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureParameterValues"
SSM_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureParameterMapping"
SSB_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureSignalDictionary"
OMS_NAMESPACE = "https://raw.githubusercontent.com/OpenModelica/OMSimulator/master/schema/oms.xsd"

ET.register_namespace("ssd", SSD_NAMESPACE)
ET.register_namespace("ssc", SSC_NAMESPACE)
ET.register_namespace("ssv", SSV_NAMESPACE)
ET.register_namespace("ssm", SSM_NAMESPACE)
ET.register_namespace("ssb", SSB_NAMESPACE)
ET.register_namespace("oms", OMS_NAMESPACE)

MODEL_CLASS_MAP: Dict[str, str] = {
    "CompositeAirframe": "Aircraft.CompositeAirframe",
    "TurbofanPropulsion": "Aircraft.TurbofanPropulsion",
    "AdaptiveWingSystem": "Aircraft.AdaptiveWingSystem",
    "MissionComputer": "Aircraft.MissionComputer",
    "AutopilotModule": "Aircraft.AutopilotModule",
    "FuelSystem": "Aircraft.FuelSystem",
    "ControlInterface": "Aircraft.ControlInterface",
}


def fmu_source(component_name: str) -> str:
    modelica_class = MODEL_CLASS_MAP.get(component_name)
    if not modelica_class:
        raise KeyError(f"No Modelica class map defined for component '{component_name}'")
    fmu_filename = modelica_class.replace(".", "_") + ".fmu"
    return f"resources/{fmu_filename}"


def _unique_component_name(name: str, used: Dict[str, str]) -> str:
    base = "".join(ch if ch.isalnum() else "_" for ch in name).strip("_") or "Component"
    candidate = base
    suffix = 2
    while candidate in used.values():
        candidate = f"{base}{suffix}"
        suffix += 1
    return candidate


def _connector_kind(direction: str) -> Optional[str]:
    if direction == "in":
        return "input"
    if direction == "out":
        return "output"
    return None


def _ensure_connectors_element(component_elem: ET.Element) -> ET.Element:
    connectors_elem = component_elem.find(f"{{{SSD_NAMESPACE}}}Connectors")
    if connectors_elem is None:
        connectors_elem = ET.SubElement(component_elem, f"{{{SSD_NAMESPACE}}}Connectors")
    return connectors_elem


def _add_terminal_connector(component_elem: ET.Element, port_name: str, kind: str) -> None:
    connectors_elem = _ensure_connectors_element(component_elem)
    connector_elem = ET.SubElement(
        connectors_elem,
        f"{{{SSD_NAMESPACE}}}Connector",
        attrib={"name": port_name, "kind": kind},
    )
    ET.SubElement(connector_elem, f"{{{SSC_NAMESPACE}}}Terminal")


def build_terminal_ssd_tree(architecture: SysMLArchitecture) -> ET.ElementTree:
    system_name = architecture.package or "System"
    components = [(name, part) for name, part in architecture.parts.items() if name != system_name]
    component_names: Dict[str, str] = {}

    root = ET.Element(
        f"{{{SSD_NAMESPACE}}}SystemStructureDescription",
        attrib={
            "name": system_name,
            "version": "1.0",
        },
    )
    system_elem = ET.SubElement(root, f"{{{SSD_NAMESPACE}}}System", attrib={"name": "root"})
    elements_elem = ET.SubElement(system_elem, f"{{{SSD_NAMESPACE}}}Elements")

    for part_name, part in components:
        display_name = _unique_component_name(part_name, component_names)
        component_names[part_name] = display_name
        component_elem = ET.SubElement(
            elements_elem,
            f"{{{SSD_NAMESPACE}}}Component",
            attrib={
                "name": display_name,
                "type": "application/x-fmu-sharedlibrary",
                "source": fmu_source(part_name),
            },
        )
        for port in part.ports:
            kind = _connector_kind(port.direction)
            if not kind:
                continue
            _add_terminal_connector(component_elem, port.name, kind)

    connections_elem = ET.SubElement(system_elem, f"{{{SSD_NAMESPACE}}}Connections")
    for conn in architecture.connections:
        start_element = component_names.get(conn.src_component)
        end_element = component_names.get(conn.dst_component)
        if not start_element or not end_element:
            continue
        ET.SubElement(
            connections_elem,
            f"{{{SSD_NAMESPACE}}}Connection",
            attrib={
                "startElement": start_element,
                "startConnector": conn.src_port,
                "endElement": end_element,
                "endConnector": conn.dst_port,
            },
        )

    ET.SubElement(
        root,
        f"{{{SSD_NAMESPACE}}}DefaultExperiment",
        attrib={"startTime": "0.0", "stopTime": "3600.0"},
    )

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    return tree


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Path to the SysML architecture directory or a file within it.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination file for the generated SSD.",
    )
    args = parser.parse_args(argv)

    source = args.architecture
    if source.is_file():
        source = source.parent

    try:
        architecture = parse_sysml_folder(source)
        tree = build_terminal_ssd_tree(architecture)
    ensure_parent_dir(args.output)
        tree.write(args.output, encoding="utf-8", xml_declaration=True)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
