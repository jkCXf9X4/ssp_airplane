"""Helpers for exporting SysML architecture interfaces to C/C++ artifacts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from pycps_sysmlv2 import NodeType, SysMLPartDefinition, SysMLPortDefinition

from scripts.lib.paths import COMPOSITION_NAME
from scripts.lib.sysml.type_utils import infer_primitive, normalize_primitive
from scripts.lib.sysml.values import parse_literal


@dataclass(frozen=True)
class VariableSpec:
    name: str
    value_reference: int
    fmi_type: str
    causality: str
    variability: Optional[str] = None
    start_value: Optional[str] = None
    c_member_type: str = "double"
    cpp_member_type: str = "double"
    field_path: str = ""


def c_primitive(type_name: str) -> str:
    primitive = normalize_primitive(type_name)
    return {
        "Real": "double",
        "Integer": "int",
        "Boolean": "bool",
        "String": "const char*",
    }.get(primitive, "double")


def cpp_member_type(type_name: str) -> str:
    primitive = normalize_primitive(type_name)
    return {
        "Real": "double",
        "Integer": "int",
        "Boolean": "bool",
        "String": "std::string",
    }.get(primitive, "double")


def sanitize_c_identifier(name: str) -> str:
    chars = []
    for char in name:
        if char.isalnum():
            chars.append(char.upper())
        else:
            chars.append("_")
    return "".join(chars)


def port_struct_fields(port_def: SysMLPortDefinition) -> List[tuple[str, str]]:
    fields: List[tuple[str, str]] = []
    for attr in port_def.defs(NodeType.Attribute).values():
        fields.append((attr.name, c_primitive(attr.type.as_string() or "Real")))
    return fields


def format_cpp_default(type_name: str, value: object | None) -> str:
    primitive = normalize_primitive(type_name)
    if value is None or isinstance(value, list):
        return "{}"
    if primitive != "String" and isinstance(value, str) and value.strip().startswith("[") and value.strip().endswith("]"):
        return "{}"
    if primitive == "Boolean":
        return "true" if bool(value) else "false"
    if primitive == "String":
        escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return str(value)


def part_variable_specs(part: SysMLPartDefinition) -> List[VariableSpec]:
    specs: List[VariableSpec] = []
    value_reference = 0

    for attr in part.defs(NodeType.Attribute).values():
        literal = parse_literal(attr.value)
        primitive = infer_primitive(attr.type, literal)
        start_value = None
        if literal is not None and not isinstance(literal, list):
            if primitive == "Boolean":
                start_value = "true" if bool(literal) else "false"
            else:
                start_value = str(literal)
        specs.append(
            VariableSpec(
                name=attr.name,
                value_reference=value_reference,
                fmi_type=primitive,
                causality="parameter",
                variability="fixed",
                start_value=start_value,
                c_member_type=c_primitive(attr.type.as_string() or primitive),
                cpp_member_type=cpp_member_type(attr.type.as_string() or primitive),
                field_path=attr.name,
            )
        )
        value_reference += 1

    for port in part.refs(NodeType.Port).values():
        payload = port.ref_node
        if payload is None:
            continue
        for attr in payload.defs(NodeType.Attribute).values():
            specs.append(
                VariableSpec(
                    name=f"{port.name}.{attr.name}",
                    value_reference=value_reference,
                    fmi_type=normalize_primitive(attr.type),
                    causality="input" if port.direction == "in" else "output",
                    c_member_type=c_primitive(attr.type.as_string() or "Real"),
                    cpp_member_type=cpp_member_type(attr.type.as_string() or "Real"),
                    field_path=f"{port.name}.{attr.name}",
                )
            )
            value_reference += 1

    return specs


def architecture_part_specs(architecture) -> Dict[str, List[VariableSpec]]:
    return {
        name: part_variable_specs(part)
        for name, part in architecture.part_definitions.items()
        if name != COMPOSITION_NAME
    }


def output_indexes(specs: Iterable[VariableSpec]) -> List[int]:
    indexes: List[int] = []
    for idx, spec in enumerate(specs, start=1):
        if spec.causality == "output":
            indexes.append(idx)
    return indexes


def part_instance_fields(package: str, part: SysMLPartDefinition) -> List[tuple[str, str, str]]:
    fields: List[tuple[str, str, str]] = []
    for attr in part.defs(NodeType.Attribute).values():
        literal = parse_literal(attr.value)
        primitive = infer_primitive(attr.type, literal)
        fields.append(
            (
                cpp_member_type(attr.type.as_string() or primitive),
                attr.name,
                format_cpp_default(attr.type.as_string() or primitive, literal),
            )
        )
    for port in part.refs(NodeType.Port).values():
        if port.ref_node is None:
            continue
        fields.append((f"{package}_{port.ref_node.name}", port.name, "{}"))
    return fields


def binding_offset_expression(package: str, part: SysMLPartDefinition, spec: VariableSpec) -> str:
    instance_name = f"{package}_{part.name}_Instance"
    if "." not in spec.field_path:
        return f"offsetof({instance_name}, {spec.field_path})"
    head, tail = spec.field_path.split(".", 1)
    payload_name = next(
        port.ref_node.name
        for port in part.refs(NodeType.Port).values()
        if port.name == head and port.ref_node is not None
    )
    return (
        f"offsetof({instance_name}, {head}) + "
        f"offsetof({package}_{payload_name}, {tail})"
    )
