#!/usr/bin/env python3
"""Generate a compact SSD that relies on FMI terminals for structured connectors."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Optional
from lxml import etree as ET
from lxml.etree import QName

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from pyssp_standard.ssd import Component, Connection, Connector, DefaultExperiment, SSD, System
from scripts.common.fmi_helpers import architecture_model_map, component_fmu_source
from pycps_sysmlv2 import SysMLArchitecture, load_architecture
from scripts.common.sysml import (
    architecture_connections,
    architecture_package,
    composition_components,
    part_ports,
)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "SystemStructure_terminals.ssd"

SSC_NAMESPACE = "http://ssp-standard.org/SSP1/SystemStructureCommon"


def _unique_component_name(name: str, used: Dict[str, str]) -> str:
    base = "".join(ch if ch.isalnum() else "_" for ch in name).strip("_") or "Component"
    candidate = base
    suffix = 2
    while candidate in used.values():
        candidate = f"{base}{suffix}"
        suffix += 1
    return candidate


class _TerminalType:
    def to_xml(self, namespace: str = "ssc"):
        if namespace != "ssc":
            raise ValueError("Terminal connectors are only supported in SSP common namespace.")
        return ET.Element(QName(SSC_NAMESPACE, "Terminal"))


def build_terminal_ssd(
    ssd: SSD,
    architecture: SysMLArchitecture,
    class_map: Optional[Dict[str, str]] = None,
) -> None:
    system_name = architecture_package(architecture) or "System"
    components = composition_components(architecture)
    component_names: Dict[str, str] = {}
    class_map = class_map or architecture_model_map(architecture)

    ssd.name = system_name
    ssd.version = "1.0"
    ssd.system = System(name="root")

    for part_name, part in components:
        display_name = _unique_component_name(part_name, component_names)
        component_names[part_name] = display_name
        component = Component()
        component.name = display_name
        component.component_type = "application/x-fmu-sharedlibrary"
        component.source = component_fmu_source(part.name, class_map)
        for port in part_ports(part):
            if port.direction == "in":
                kind = "input"
            elif port.direction == "out":
                kind = "output"
            else:
                continue
            component.connectors.append(
                Connector(
                    name=port.name,
                    kind=kind,
                    type_=_TerminalType(),
                )
            )
        ssd.system.elements.append(component)

    for conn in architecture_connections(architecture):
        start_element = component_names.get(conn.src_component)
        end_element = component_names.get(conn.dst_component)
        if not start_element or not end_element:
            continue
        ssd.add_connection(
            Connection(
                start_element=start_element,
                start_connector=conn.src_port,
                end_element=end_element,
                end_connector=conn.dst_port,
            )
        )

    default_experiment = DefaultExperiment()
    default_experiment.start_time = 0.0
    default_experiment.stop_time = 3600.0
    ssd.default_experiment = default_experiment


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

    try:
        architecture = load_architecture(args.architecture)
        ensure_parent_dir(args.output)
        with SSD(args.output, mode="w") as ssd:
            build_terminal_ssd(ssd, architecture)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
