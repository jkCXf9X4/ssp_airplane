"""Compatibility accessors that smooth over parser object differences."""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace


@dataclass(frozen=True)
class LegacyAttribute:
    name: str
    type: str | None


@dataclass(frozen=True)
class LegacyPortDefinition:
    name: str
    attributes: dict


def architecture_port_definitions(architecture):
    port_definitions = getattr(architecture, "port_definitions", {})
    translated = {}
    for name, port_def in port_definitions.items():
        translated[name] = LegacyPortDefinition(
            name=name,
            attributes={
                attr_name: LegacyAttribute(
                    name=attr_name,
                    type=getattr(attr.type, "as_string", lambda: attr.type)(),
                )
                for attr_name, attr in port_def.attributes.items()
            },
        )
    return translated


def architecture_connections(architecture):
    connections = getattr(architecture, "connections", [])
    references = getattr(architecture, "part_references", {})
    if not references:
        return connections

    translated = []
    for connection in connections:
        src_ref = references.get(connection.src_component)
        dst_ref = references.get(connection.dst_component)
        translated.append(
            replace(
                connection,
                src_component=getattr(src_ref, "part_name", connection.src_component),
                dst_component=getattr(dst_ref, "part_name", connection.dst_component),
            )
        )
    return translated
