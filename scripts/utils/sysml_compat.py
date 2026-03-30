"""Compatibility accessors that smooth over parser object differences."""
from __future__ import annotations

from dataclasses import dataclass

from pycps_sysmlv2 import NodeType


@dataclass(frozen=True)
class LegacyAttribute:
    name: str
    type: str | None


@dataclass(frozen=True)
class LegacyPortDefinition:
    name: str
    attributes: dict


@dataclass(frozen=True)
class LegacyConnection:
    src_component: str
    src_port: str
    dst_component: str
    dst_port: str


def architecture_port_definitions(architecture):
    port_definitions = getattr(architecture, "port_definitions", {})
    translated = {}
    for name, port_def in port_definitions.items():
        translated[name] = LegacyPortDefinition(
            name=name,
            attributes={
                attr_name: LegacyAttribute(
                    name=attr_name,
                    type=attr.type.as_string(),
                )
                for attr_name, attr in port_def.defs(NodeType.Attribute).items()
            },
        )
    return translated


def architecture_connections(architecture):
    connections = getattr(architecture, "connections", [])
    references = getattr(architecture, "part_references", {})
    translated = []
    for connection in connections:
        src_ref = references.get(connection.src_part)
        dst_ref = references.get(connection.dst_part)
        translated.append(
            LegacyConnection(
                src_component=getattr(getattr(src_ref, "ref_node", None), "name", connection.src_part),
                src_port=connection.src_port,
                dst_component=getattr(getattr(dst_ref, "ref_node", None), "name", connection.dst_part),
                dst_port=connection.dst_port,
            )
        )
    return translated
