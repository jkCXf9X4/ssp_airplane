"""Helpers for normalizing SysML primitive type names."""
from __future__ import annotations

from typing import Optional

PRIMITIVE_TYPE_MAP = {
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


def _type_key(type_name: Optional[object]) -> Optional[str]:
    if not type_name:
        return None
    if hasattr(type_name, "as_string"):
        type_name = type_name.as_string()
    if not isinstance(type_name, str):
        type_name = str(type_name)
    return type_name.strip().lower()


def normalize_primitive(type_name: Optional[str], default: str = "Real") -> str:
    """Return a canonical primitive name (Real/Integer/Boolean/String) for SysML types."""
    key = _type_key(type_name)
    if not key:
        return default
    return PRIMITIVE_TYPE_MAP.get(key, default)


def optional_primitive(type_name: Optional[str]) -> Optional[str]:
    """Return the canonical primitive name or None if the type is unset/unknown."""
    key = _type_key(type_name)
    if not key:
        return None
    return PRIMITIVE_TYPE_MAP.get(key)


def modelica_connector_type(type_name: Optional[str]) -> str:
    """Map SysML types to Modelica connector primitives, preserving custom names."""
    key = _type_key(type_name)
    if not key:
        return "Real"
    if hasattr(type_name, "as_string"):
        type_name = type_name.as_string()
    return PRIMITIVE_TYPE_MAP.get(key, type_name)


def primitive_from_value(value: Optional[object]) -> Optional[str]:
    """Infer a primitive type from a literal value."""
    if isinstance(value, bool):
        return "Boolean"
    if isinstance(value, int):
        return "Integer"
    if isinstance(value, float):
        return "Real"
    if isinstance(value, str):
        return "String"
    return None


def infer_primitive(attr_type: Optional[str], sample: Optional[object], default: str = "Real") -> str:
    """Infer primitive from an explicit type hint or fallback sample value."""
    normalized = optional_primitive(attr_type)
    if normalized:
        return normalized
    inferred = primitive_from_value(sample)
    if inferred:
        return inferred
    return default
