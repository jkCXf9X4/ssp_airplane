"""Shared helper utilities for working with SysML architectures."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

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


def _legacy_part(part_def) -> LegacyPartDefinition:
    ports = [
        LegacyPortReference(
            name=port.name,
            direction=port.direction,
            payload=port.port_name,
            payload_def=port.port_def,
            doc=getattr(port, "doc", None),
        )
        for port in part_def.ports.values()
    ]
    return LegacyPartDefinition(
        name=part_def.name,
        attributes=part_def.attributes,
        ports=ports,
        doc=getattr(part_def, "doc", None),
    )


def _legacy_view(path: Path):
    from pycps_sysmlv2 import load_architecture as _load_architecture
    from pycps_sysmlv2 import load_system

    architecture = _load_architecture(path)
    system = load_system(path, COMPOSITION_NAME)

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
        part_references=dict(system.parts),
        connections=list(system.connections),
        requirements=getattr(architecture, "requirements", {}),
    )


def load_architecture(source: Path):
    """Load a SysML architecture from either a directory or a file within it."""
    path = source
    if path.is_file():
        path = path.parent

    try:
        return _legacy_view(path)
    except ModuleNotFoundError:
        from sysml import load_architecture as _load_architecture  # type: ignore

    return _load_architecture(path)


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
