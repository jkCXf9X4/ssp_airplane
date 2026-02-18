"""Compatibility helpers for the extracted SysML package surface."""
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from pycps_sysmlv2 import (
    SysMLArchitecture,
    SysMLConnection,
    SysMLPartDefinition,
    SysMLPortReference,
    SysMLPortDefinition,
)
from pycps_sysmlv2.type_utils import parse_literal

from scripts.common.paths import COMPOSITION_NAME


def select_parts(architecture: SysMLArchitecture, parts: List[str]):
    return [x for x in architecture.part_definitions.values() if x.name in parts]


# All shpould be removed

def architecture_port_definitions(
    architecture: SysMLArchitecture,
) -> Dict[str, SysMLPortDefinition]:
    """Return the parsed port-definition map."""
    port_definitions = getattr(architecture, "port_definitions", None)
    if port_definitions is None:
        port_definitions = getattr(architecture, "_port_definitions", None)
    if port_definitions is None:
        raise AttributeError("SysMLArchitecture does not expose port definitions.")
    return port_definitions


def architecture_package(architecture: SysMLArchitecture) -> str:
    """Return the SysML package name."""
    return architecture.package


def architecture_connections(architecture: SysMLArchitecture) -> List[SysMLConnection]:
    """Return connections declared on the composition part."""
    return composition_connections(architecture)


def literal_value(value: object) -> object:
    """Return a parsed literal while preserving already-parsed values."""
    if isinstance(value, str):
        return parse_literal(value)
    return value


def composition_components(
    architecture: SysMLArchitecture,
) -> List[Tuple[str, SysMLPartDefinition]]:
    """Return instance-name to part-definition pairs from the composition part."""
    composition = composition_part(architecture)
    if not composition.parts:
        raise ValueError(
            "Composition part has no child part instances."
        )

    resolved: List[Tuple[str, SysMLPartDefinition]] = []
    for instance in _iter_part_instances(composition.parts):
        target_def = instance.target_def
        if target_def is None:
            raise ValueError(
                f"Composition instance '{instance.name}' references unknown part definition '{instance.target}'."
            )
        resolved.append((instance.name, target_def))
    return resolved


def composition_connections(architecture: SysMLArchitecture) -> List[SysMLConnection]:
    """Return connections declared on the composition part."""
    composition = composition_part(architecture)
    return list(composition.connections)


def part_ports(part: SysMLPartDefinition) -> List[SysMLPortReference]:
    """Return part ports from either dict or list structures."""
    ports = part.ports
    if isinstance(ports, dict):
        return list(ports.values())
    return list(ports)


def composition_part(architecture: SysMLArchitecture) -> SysMLPartDefinition:
    """Return the composition basis part definition."""
    part_definitions = getattr(architecture, "part_definitions", None)
    if part_definitions is None:
        part_definitions = getattr(architecture, "parts", None)
    if part_definitions is None:
        raise AttributeError("SysMLArchitecture does not expose part definitions.")


    composition = part_definitions.get(COMPOSITION_NAME)
    if composition is not None:
        return composition
    
    raise ValueError(
        "Required composition part not found. Expected one of: "
        + ", ".join(COMPOSITION_NAME)
    )


def _iter_part_instances(parts: object) -> Iterable[object]:
    """Yield part-reference instances from either dict or list structures."""
    if isinstance(parts, dict):
        return parts.values()
    return parts

