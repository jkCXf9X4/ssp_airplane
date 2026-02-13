"""Compatibility helpers for the extracted SysML package surface."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from sysml import SysMLArchitecture, SysMLConnection, SysMLPortDefinition
from sysml.type_utils import parse_literal

_CONNECTION_RE = re.compile(
    r"connect\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\s+to\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\s*;"
)


def architecture_port_definitions(
    architecture: SysMLArchitecture,
) -> Dict[str, SysMLPortDefinition]:
    """Return the parsed port-definition map."""
    return architecture._port_definitions


def architecture_connections(architecture: SysMLArchitecture) -> List[SysMLConnection]:
    """Return deduplicated connections declared across all parsed parts."""
    connections: List[SysMLConnection] = []
    seen: set[Tuple[str, str, str, str]] = set()
    for part in architecture.parts.values():
        for connection in part.connections:
            key = (
                connection.src_component,
                connection.src_port,
                connection.dst_component,
                connection.dst_port,
            )
            if key in seen:
                continue
            seen.add(key)
            connections.append(connection)
    for connection in _scan_package_connections(architecture):
        key = (
            connection.src_component,
            connection.src_port,
            connection.dst_component,
            connection.dst_port,
        )
        if key in seen:
            continue
        seen.add(key)
        connections.append(connection)
    return connections


def literal_value(value: object) -> object:
    """Return a parsed literal while preserving already-parsed values."""
    if isinstance(value, str):
        return parse_literal(value)
    return value


def _scan_package_connections(architecture: SysMLArchitecture) -> List[SysMLConnection]:
    candidates = _candidate_arch_dirs()
    for folder in candidates:
        if not folder.exists():
            continue
        found: List[SysMLConnection] = []
        for sysml_path in sorted(folder.glob("*.sysml")):
            text = sysml_path.read_text()
            for match in _CONNECTION_RE.finditer(text):
                found.append(
                    SysMLConnection(
                        src_component=match.group(1),
                        src_port=match.group(2),
                        dst_component=match.group(3),
                        dst_port=match.group(4),
                    )
                )
        if found:
            return found
    return []


def _candidate_arch_dirs() -> List[Path]:
    return [
        Path("architecture"),
        Path(__file__).resolve().parents[2] / "architecture",
    ]
