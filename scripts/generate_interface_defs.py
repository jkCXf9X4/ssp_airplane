#!/usr/bin/env python3
"""Emit interface definitions for SysML data-def types as Modelica records."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

from scripts.utils.sysmlv2_arch_parser import SysMLArchitecture, SysMLPortDefinition, parse_sysml_folder

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCH_PATH = REPO_ROOT / "architecture"
OUTPUT_DIR = REPO_ROOT / "generated" 

PRIMITIVE_MAP = {
    "real": "Real",
    "float": "Real",
    "float32": "Real",
    "double": "Real",
    "integer": "Integer",
    "int": "Integer",
    "int8": "Integer",
    "uint8": "Integer",
    "boolean": "Boolean",
    "bool": "Boolean",
}


def _collect_data_defs(architecture: SysMLArchitecture) -> Dict[str, List[Tuple[str, str]]]:
    defs: Dict[str, List[Tuple[str, str]]] = {}
    for name, port_def in architecture.port_definitions.items():
        defs[name] = _port_attributes(port_def)
    return defs


def _port_attributes(port_def: SysMLPortDefinition) -> List[Tuple[str, str]]:
    attrs: List[Tuple[str, str]] = []
    for attr in port_def.attributes.values():
        attr_type = attr.type or "Real"
        attrs.append((attr.name, attr_type))
    return attrs


def to_modelica_type(sysml_type: str) -> str:
    return PRIMITIVE_MAP.get(sysml_type.lower(), sysml_type)


def generate_modelica_package(defs: Dict[str, List[Tuple[str, str]]]) -> str:
    lines = ["within WingmanDrone;", "package GeneratedInterfaces"]
    for type_name, fields in sorted(defs.items()):
        lines.append(f"  record {type_name}")
        if not fields:
            lines.append(f"  end {type_name};")
            continue
        for field, field_type in fields:
            mo_type = to_modelica_type(field_type)
            lines.append(f"    {mo_type} {field};")
        lines.append(f"  end {type_name};")
        lines.append("")
    lines.append("end GeneratedInterfaces;")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=ARCH_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR / "GeneratedInterfaces.mo")
    args = parser.parse_args()

    architecture = parse_sysml_folder(args.architecture)
    data_defs = _collect_data_defs(architecture)
    if not data_defs:
        raise SystemExit("No data definitions found; nothing to generate.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = generate_modelica_package(data_defs)
    args.output.write_text(content)
    print(f"Wrote Modelica interfaces to {args.output}")


if __name__ == "__main__":
    main()
