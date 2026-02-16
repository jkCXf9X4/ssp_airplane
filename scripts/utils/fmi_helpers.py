"""Utility helpers for working with FMI artifacts derived from Modelica classes."""
from __future__ import annotations

from typing import Dict, Optional


def fmu_filename(modelica_class: str) -> str:
    """Return the FMU filename for a fully-qualified Modelica class."""
    return modelica_class.replace(".", "_") + ".fmu"


def fmu_resource_path(modelica_class: str) -> str:
    """Return the SSP resources relative path for an FMU."""
    return f"resources/{fmu_filename(modelica_class)}"


FMI_TYPE_MAP = {
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

def map_fmi_type(type_name: Optional[str], default: str = "Real") -> str:
    """Return a canonical primitive name (Real/Integer/Boolean/String) for SysML types."""
    if not type_name:
        return default
    key = type_name.strip().lower()
    return FMI_TYPE_MAP.get(key, default)


def format_start_value(fmi_type: str, literal: Optional[object]) -> Optional[str]:
    if literal is None:
        return None
    if fmi_type == "Real":
        return f"{float(literal):g}"
    if fmi_type == "Integer":
        return str(int(literal))
    if fmi_type == "Boolean":
        return "true" if bool(literal) else "false"
    if fmi_type == "String":
        return str(literal)
    return None

# def architecture_model_map(architecture: SysMLArchitecture) -> Dict[str, str]:
#     """Convenience wrapper to build the part->Modelica class mapping."""
#     return component_modelica_map(architecture)


# def component_fmu_source(component_name: str, class_map: Dict[str, str]) -> str:
#     """Resolve the FMU resource path for a given component."""
#     modelica_class = class_map.get(component_name)
#     if not modelica_class:
#         raise KeyError(f"No Modelica class map defined for component '{component_name}'")
#     return fmu_resource_path(modelica_class)
