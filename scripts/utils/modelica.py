"""Shared helper utilities for working with SysML architectures."""
from __future__ import annotations

from typing import Dict, Optional

from pycps_sysmlv2 import SysMLArchitecture
from scripts.utils.sysml_compat import architecture_package, composition_components


def component_modelica_map(
    architecture: SysMLArchitecture, package_override: Optional[str] = None
) -> Dict[str, str]:
    """Build a mapping from composition instance names to Modelica classes."""
    package = package_override or architecture_package(architecture) or "System"
    mapping: Dict[str, str] = {}
    for instance_name, target_def in composition_components(architecture):
        mapping[instance_name] = f"{package}.{target_def.name}"
    return mapping
