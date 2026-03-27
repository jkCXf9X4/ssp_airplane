"""Helpers for exporting architecture interfaces to C-compatible artifacts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from scripts.common.sysml_values import parse_literal
from scripts.utils.sysmlv2_arch_parser import SysMLArchitecture, SysMLPartDefinition, SysMLPortDefinition
from scripts.utils.type_utils import infer_primitive, normalize_primitive


@dataclass(frozen=True)
class VariableSpec:
    name: str
    value_reference: int
    fmi_type: str
    causality: str
    variability: Optional[str] = None
    start_value: Optional[str] = None


def c_primitive(type_name: str) -> str:
    primitive = normalize_primitive(type_name)
    return {
        "Real": "double",
        "Integer": "int",
        "Boolean": "bool",
        "String": "const char*",
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
    for attr in port_def.attributes.values():
        fields.append((attr.name, c_primitive(attr.type or "Real")))
    return fields


def part_variable_specs(part: SysMLPartDefinition) -> List[VariableSpec]:
    specs: List[VariableSpec] = []
    value_reference = 0

    for attr in part.attributes.values():
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
            )
        )
        value_reference += 1

    for port in part.ports:
        payload = port.payload_def
        if payload is None:
            continue
        for attr in payload.attributes.values():
            specs.append(
                VariableSpec(
                    name=f"{port.name}.{attr.name}",
                    value_reference=value_reference,
                    fmi_type=normalize_primitive(attr.type),
                    causality="input" if port.direction == "in" else "output",
                )
            )
            value_reference += 1

    return specs


def architecture_part_specs(architecture: SysMLArchitecture) -> Dict[str, List[VariableSpec]]:
    return {name: part_variable_specs(part) for name, part in architecture.parts.items()}


def output_indexes(specs: Iterable[VariableSpec]) -> List[int]:
    indexes: List[int] = []
    for idx, spec in enumerate(specs, start=1):
        if spec.causality == "output":
            indexes.append(idx)
    return indexes
