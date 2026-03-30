"""Shared helper utilities for working with SysML architectures."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from pycps_sysmlv2 import NodeType, SysMLParser

from scripts.common.paths import COMPOSITION_NAME


@dataclass(frozen=True)
class LegacyArchitectureView:
    package: str
    part_definitions: dict
    port_definitions: dict
    parts: dict
    part_references: dict
    connections: list
    requirements: dict


@dataclass(frozen=True)
class LegacyPortReference:
    name: str
    direction: str
    payload: str
    payload_def: object
    doc: str | None = None


@dataclass(frozen=True)
class LegacyPartDefinition:
    name: str
    attributes: dict
    ports: list[LegacyPortReference]
    doc: str | None = None


@dataclass(frozen=True)
class LegacyPortDefinition:
    name: str
    attributes: dict
    doc: str | None = None


def _legacy_port_definition(port_def):
    if port_def is None:
        return None
    return LegacyPortDefinition(
        name=port_def.name,
        attributes=port_def.defs(NodeType.Attribute),
        doc=getattr(port_def, "doc", None),
    )


def _legacy_part(part_def) -> LegacyPartDefinition:
    ports = [
        LegacyPortReference(
            name=port.name,
            direction=port.direction,
            payload=port.type,
            payload_def=_legacy_port_definition(port.ref_node),
            doc=getattr(port, "doc", None),
        )
        for port in part_def.refs(NodeType.Port).values()
    ]
    return LegacyPartDefinition(
        name=part_def.name,
        attributes=part_def.defs(NodeType.Attribute),
        ports=ports,
        doc=getattr(part_def, "doc", None),
    )


def _legacy_view(path: Path):
    architecture = SysMLParser(path).parse()
    system = architecture.get_def(NodeType.Part, COMPOSITION_NAME)

    parts = {
        name: _legacy_part(part_def)
        for name, part_def in architecture.part_definitions.items()
        if name != COMPOSITION_NAME
    }

    return LegacyArchitectureView(
        package=architecture.package,
        part_definitions=architecture.part_definitions,
        port_definitions=architecture.port_definitions,
        parts=parts,
        part_references=dict(system.refs(NodeType.Part)),
        connections=list(system.defs(NodeType.Connection).values()),
        requirements=getattr(architecture, "requirement_definitions", {}),
    )


def load_architecture(source: Path | str):
    """Load a SysML architecture from either a directory or a file within it."""
    path = Path(source)
    if path.is_file():
        path = path.parent
    return _legacy_view(path)


def component_modelica_map(
    architecture, package_override: Optional[str] = None
) -> Dict[str, str]:
    """Build a mapping from component names to fully-qualified Modelica classes."""
    package = package_override or getattr(architecture, "package", None) or "System"
    mapping: Dict[str, str] = {}
    for name in architecture.parts:
        if name == package:
            continue
        mapping[name] = f"{package}.{name}"
    return mapping
