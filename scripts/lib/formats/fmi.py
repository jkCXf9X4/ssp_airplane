"""Helpers for working with FMI artifact naming and primitive types."""
from __future__ import annotations

from typing import Optional

from scripts.lib.sysml.type_utils import normalize_primitive


def fmu_filename(modelica_class: str) -> str:
    """Return the FMU filename for a fully-qualified Modelica class."""
    return modelica_class.replace(".", "_") + ".fmu"


def fmu_resource_path(modelica_class: str) -> str:
    """Return the SSP resources relative path for an FMU."""
    return f"resources/{fmu_filename(modelica_class)}"


def map_fmi_type(type_name: Optional[str], default: str = "Real") -> str:
    """Return a canonical FMI primitive name (Real/Integer/Boolean/String)."""
    return normalize_primitive(type_name, default)


def format_value(tag: str, literal):
    if literal is None:
        return ""
    if tag == "Real":
        return f"{float(literal):g}"
    if tag == "Integer":
        return str(int(literal))
    if tag == "Boolean":
        return "true" if bool(literal) else "false"
    if tag == "String":
        return str(literal)
    raise ValueError(f"Unknown FMI tag: {tag}")


def to_fmi_direction_definition(direction: str):
    if direction == "in":
        return "input"
    if direction == "out":
        return "output"
    raise ValueError(f"Unknown direction: {direction}")
