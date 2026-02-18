#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from pyssp_standard.common_content_ssc import TypeBoolean, TypeInteger, TypeReal, TypeString
from pyssp_standard.ssd import Component, Connection, Connector, DefaultExperiment, SSD, System
from pycps_sysmlv2 import (
    SysMLArchitecture,
    SysMLAttribute,
    SysMLPortDefinition,
    SysMLPortReference,
    load_architecture,
)
from pycps_sysmlv2.type_utils import infer_primitive, normalize_primitive
from scripts.common.fmi_helpers import architecture_model_map, component_fmu_source
from scripts.common.sysml import (
    architecture_package,
    architecture_connections,
    composition_components,
    architecture_port_definitions,
    literal_value,
    part_ports,
)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "SystemStructure.ssd"


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
            entries.append((attr.name, normalize_primitive(attr.type)))
    if not entries:
        entries.append(("", "Real"))
    return entries


def _expand_port_entries(
    port: SysMLPortReference, architecture: SysMLArchitecture
) -> List[Dict[str, str]]:
    if port.direction not in {"in", "out"}:
        return []
    kind = "input" if port.direction == "in" else "output"
    payload_entries = _expand_payload_definition(
        port.payload_def,
        architecture_port_definitions(architecture),
    )
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
        literal = literal_value(attr.value)
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


def _type_from_primitive(primitive: str):
    normalized = normalize_primitive(primitive)
    if normalized == "Real":
        return TypeReal(unit=None)
    if normalized == "Integer":
        return TypeInteger()
    if normalized == "Boolean":
        return TypeBoolean()
    if normalized == "String":
        return TypeString()
    return TypeReal(unit=None)


def build_ssd(
    ssd: SSD,
    architecture: SysMLArchitecture,
    class_map: Optional[Dict[str, str]] = None,
) -> None:
    class_map = class_map or architecture_model_map(architecture)
    system_name = architecture_package(architecture)
    components = composition_components(architecture)
    component_names: Dict[str, str] = {}
    connector_lookup: Dict[str, Dict[str, Dict[str, str]]] = {}

    ssd.name = system_name
    ssd.version = "1.0"
    ssd.system = System(name=system_name)

    for part_name, part in components:
        component_names[part_name] = _unique_component_name(part_name, component_names)
        display_name = component_names[part_name]
        component = Component()
        component.name = display_name
        component.component_type = "application/x-fmu-sharedlibrary"
        component.source = component_fmu_source(part.name, class_map)

        connector_entries: List[Dict[str, str]] = []
        port_map: Dict[str, Dict[str, str]] = {}
        for port in part_ports(part):
            entries = _expand_port_entries(port, architecture)
            if not entries:
                continue
            port_map[port.name] = {
                entry["suffix"]: entry["connector_name"] for entry in entries
            }
            connector_entries.extend(entries)

        parameter_entries = _parameter_connector_entries(part.attributes)

        for entry in connector_entries:
            component.connectors.append(
                Connector(
                    name=entry["connector_name"],
                    kind=entry["kind"],
                    type_=_type_from_primitive(entry["primitive"]),
                )
            )
        for param in parameter_entries:
            component.connectors.append(
                Connector(
                    name=param["connector_name"],
                    kind="parameter",
                    type_=_type_from_primitive(param["primitive"]),
                )
            )

        ssd.system.elements.append(component)

        connector_lookup[part_name] = port_map

    for conn in architecture_connections(architecture):
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
            ssd.add_connection(
                Connection(
                    start_element=start_component,
                    start_connector=start_connector,
                    end_element=end_component,
                    end_connector=end_connector,
                )
            )

    default_experiment = DefaultExperiment()
    default_experiment.start_time = 0
    default_experiment.stop_time = 3600
    ssd.default_experiment = default_experiment


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Directory containing the SysML architecture (.sysml) files or a file within it.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    try:
        architecture = load_architecture(args.architecture)
        ensure_parent_dir(args.output)
        with SSD(args.output, mode="w") as ssd:
            build_ssd(ssd, architecture)

    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(f"SSD written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
