"""Shared helper utilities for working with SysML architectures."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from sysml.parser import SysMLArchitecture


def component_modelica_map(
    architecture: SysMLArchitecture, package_override: Optional[str] = None
) -> Dict[str, str]:
    """Build a mapping from component names to fully-qualified Modelica classes."""
    package = package_override or architecture.package or "System"
    mapping: Dict[str, str] = {}
    for name in architecture.parts:
        if name == package:
            continue
        mapping[name] = f"{package}.{name}"
    return mapping
