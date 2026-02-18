#!/usr/bin/env python3
"""Generate an SSP System Structure Description (SSD) from the SysML architecture."""

from __future__ import annotations

import argparse
import sys
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
from scripts.common.fmi_helpers import (
    fmu_resource_path,
    to_fmi_direction_definition,
    map_fmi_type,
)

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
from pycps_sysmlv2 import (
    SysMLArchitecture,
    SysMLAttribute,
    SysMLPortDefinition,
    SysMLPortReference,
    SysMLPartDefinition,
    SysMLPartReference,
    load_system,
)

# from scripts.common.sysml import (
#     architecture_package,
#     architecture_connections,
#     composition_components,
#     architecture_port_definitions,
#     literal_value,
#     part_ports,
# )

import logging

logging.basicConfig(level=logging.DEBUG)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "SystemStructure.ssd"


# Configure logging


# def _expand_payload_definition(
#     payload_def: Optional[SysMLPortDefinition],
#     definitions: Dict[str, SysMLPortDefinition],
#     visited: Optional[Tuple[str, ...]] = None,
# ) -> List[Tuple[str, str]]:
#     if payload_def is None:
#         return [("", "Real")]
#     visited = tuple(visited or ())
#     if payload_def.name in visited:
#         return [("", "Real")]

#     entries: List[Tuple[str, str]] = []
#     for attr in payload_def.attributes.values():
#         attr_type = attr.type or ""
#         if attr_type in definitions:
#             nested = definitions[attr_type]
#             for suffix, primitive in _expand_payload_definition(
#                 nested, definitions, visited + (payload_def.name,)
#             ):
#                 field_name = attr.name if not suffix else f"{attr.name}.{suffix}"
#                 entries.append((field_name, primitive))
#         else:
#             entries.append((attr.name, normalize_primitive(attr.type)))
#     if not entries:
#         entries.append(("", "Real"))
#     return entries


# def _expand_port_entries(
#     port: SysMLPortReference, architecture: SysMLArchitecture
# ) -> List[Dict[str, str]]:
#     if port.direction not in {"in", "out"}:
#         return []
#     kind = "input" if port.direction == "in" else "output"
#     payload_entries = _expand_payload_definition(
#         port.payload_def,
#         architecture_port_definitions(architecture),
#     )
#     results: List[Dict[str, str]] = []
#     for suffix, primitive in payload_entries:
#         connector_name = port.name if not suffix else f"{port.name}.{suffix}"
#         results.append(
#             {
#                 "connector_name": connector_name,
#                 "kind": kind,
#                 "primitive": primitive,
#                 "suffix": suffix,
#             }
#         )
#     return results


# def _parameter_connector_entries(
#     attributes: Dict[str, SysMLAttribute],
# ) -> List[Dict[str, str]]:
#     entries: List[Dict[str, str]] = []
#     for name in sorted(attributes):
#         attr = attributes[name]
#         literal = literal_value(attr.value)
#         if isinstance(literal, (list, tuple)):
#             sample = next((item for item in literal if item is not None), None)
#             primitive = infer_primitive(attr.type, sample)
#             if literal:
#                 for idx, _ in enumerate(literal, start=1):
#                     entries.append(
#                         {
#                             "connector_name": f"{attr.name}[{idx}]",
#                             "primitive": primitive,
#                         }
#                     )
#             else:
#                 entries.append({"connector_name": attr.name, "primitive": primitive})
#             continue

#         primitive = infer_primitive(attr.type, literal)
#         entries.append({"connector_name": attr.name, "primitive": primitive})
#     return entries


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

            value = attribute.value
            if not isinstance(value, list):
                value = [value]

            for idx, _ in enumerate(value, start=0):
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
    # ssd.default_experiment = DefaultExperiment(start_time=0, stop_time=3600)
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
