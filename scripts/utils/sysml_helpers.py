"""Shared helper utilities for working with SysML architectures."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from scripts.utils.sysmlv2_arch_parser import SysMLArchitecture, parse_sysml_folder


def load_architecture(source: Path) -> SysMLArchitecture:
    """Load a SysML architecture from either a directory or a file within it."""
    path = source
    if path.is_file():
        path = path.parent
    return parse_sysml_folder(path)


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
