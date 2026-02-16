"""Shared helper utilities for working with SysML architectures."""
from __future__ import annotations

from typing import Dict, Optional

from pycps_sysmlv2 import SysMLArchitecture
from scripts.utils.sysml_compat import architecture_package, composition_components


MODELICA_TYPE_MAP = {
    "real": "Real",
    "float": "Real",
    "float32": "Real",
    "float64": "Real",
    "double": "Real",
    "integer": "Integer",
    "int": "Integer",
    "int8": "Integer",
    "int32": "Integer",
    "uint8": "Integer",
    "uint32": "Integer",
    "boolean": "Boolean",
    "bool": "Boolean",
    "string": "String",
}

# def component_modelica_map(
#     package :str, : SysMLArchitecture, package_override: Optional[str] = None
# ) -> Dict[str, str]:
#     """Build a mapping from composition instance names to Modelica classes."""
#     package = package_override or architecture_package(architecture) or "System"
#     mapping: Dict[str, str] = {}
#     for instance_name, target_def in composition_components(architecture):
#         mapping[instance_name] = f"{package}.{target_def.name}"
#     return mapping




def map_modelica_type(type_name: Optional[str], default: str = "Real") -> str:
    """Return a canonical primitive name (Real/Integer/Boolean/String) for SysML types."""
    if not type_name:
        return default
    key = type_name.strip().lower()
    return MODELICA_TYPE_MAP.get(key, default)
