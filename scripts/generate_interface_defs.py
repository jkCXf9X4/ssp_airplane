#!/usr/bin/env python3
"""Emit interface definitions for SysML data-def types as Modelica records."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

from sysml_loader import get_architecture_text

ARCH_PATH = Path(__file__).resolve().parents[1] / "architecture" / "aircraft_architecture.sysml"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "build" / "interfaces"

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


def parse_data_defs(text: str) -> Dict[str, List[Tuple[str, str]]]:
    """Return {type_name: [(field, field_type), ...]} extracted from SysML."""
    defs: Dict[str, List[Tuple[str, str]]] = {}
    token = "data def"
    idx = 0
    while True:
        start = text.find(token, idx)
        if start == -1:
            break
        brace_start = text.find("{", start)
        if brace_start == -1:
            break
        header = text[start + len(token) : brace_start].strip()
        type_name = header.split()[0]
        depth = 0
        pos = brace_start
        while pos < len(text):
            char = text[pos]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    block = text[brace_start + 1 : pos]
                    defs[type_name] = _extract_attributes(block)
                    idx = pos + 1
                    break
            pos += 1
        else:
            break
    return defs


def _extract_attributes(block: str) -> List[Tuple[str, str]]:
    block = re.sub(r"/\*.*?\*/", "", block, flags=re.S)
    attrs: List[Tuple[str, str]] = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line.startswith("attribute "):
            continue
        payload = line[len("attribute ") :]
        if ":" not in payload:
            continue
        name_part, remainder = payload.split(":", 1)
        attr = name_part.strip()
        value_part = remainder.split(";", 1)[0].strip()
        if attr and value_part:
            attrs.append((attr, value_part))
    return attrs


def to_modelica_type(sysml_type: str) -> str:
    return PRIMITIVE_MAP.get(sysml_type.lower(), sysml_type)


def generate_modelica_package(defs: Dict[str, List[Tuple[str, str]]]) -> str:
    lines = ["within WingmanDrone;", "package GeneratedInterfaces"]
    for type_name, fields in sorted(defs.items()):
        lines.append(f"  record {type_name}")
        if not fields:
            lines.append("  end {type_name};")
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

    architecture_text = get_architecture_text(args.architecture)
    data_defs = parse_data_defs(architecture_text)
    if not data_defs:
        raise SystemExit("No data definitions found; nothing to generate.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = generate_modelica_package(data_defs)
    args.output.write_text(content)
    print(f"Wrote Modelica interfaces to {args.output}")


if __name__ == "__main__":
    main()
