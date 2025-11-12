#!/usr/bin/env python3
"""
Compare SysML part port definitions with Modelica model interfaces.

The script scans the architecture/aircraft_architecture.sysml file for part
definitions and their ports (including direction/type metadata) and then
looks for matching connectors inside models/WingmanDrone/*.mo. It reports
mismatches such as missing ports, direction differences, or extra connectors
that exist in the Modelica code but are not defined in the architecture.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


PORT_PATTERN = re.compile(r'(?:(in|out)\s+)?port\s+(\w+)\s*\{(.*?)\}', re.DOTALL)
ATTRIBUTE_PATTERN = re.compile(r'\s*attribute\s+(\w+)\s*=\s*([^;]+);')
PART_PATTERN = re.compile(r'part\s+def\s+(\w+)\s*\{')
MODEL_NAME_PATTERN = re.compile(r'\bmodel\s+(\w+)')
CONNECTOR_PATTERN = re.compile(r'\s*Interfaces\.(RealInput|RealOutput)\s+(\w+)')


def extract_block(text: str, brace_index: int) -> Tuple[str, int]:
    """Return the text inside the block that starts at brace_index."""
    depth = 0
    i = brace_index
    while i < len(text):
        char = text[i]
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return text[brace_index + 1 : i], i + 1
        i += 1
    raise ValueError("Unbalanced braces while extracting block")


def parse_architecture_parts(architecture_path: Path) -> Dict[str, List[Dict[str, str]]]:
    """Parse the SysML file and return a mapping of part -> list of port dicts."""
    text = architecture_path.read_text()
    parts: Dict[str, List[Dict[str, str]]] = {}
    for match in PART_PATTERN.finditer(text):
        part_name = match.group(1)
        block, _ = extract_block(text, match.end() - 1)
        ports: List[Dict[str, str]] = []
        for port_match in PORT_PATTERN.finditer(block):
            decl_direction, port_name, body = port_match.groups()
            attributes = {
                key: value.strip().strip('"')
                for key, value in ATTRIBUTE_PATTERN.findall(body)
            }
            direction = attributes.get("direction")
            if not direction and decl_direction:
                direction = "in" if decl_direction == "in" else "out"
            ports.append(
                {
                    "name": port_name,
                    "direction": direction or "",
                    "kind": attributes.get("kind", ""),
                    "type": attributes.get("type", ""),
                }
            )
        parts[part_name] = ports
    return parts


def parse_modelica_connectors(models_dir: Path) -> Dict[str, Dict[str, str]]:
    """Return a mapping of model name -> {connector_name: direction}."""
    models: Dict[str, Dict[str, str]] = {}
    for mo_file in models_dir.glob("*.mo"):
        text = mo_file.read_text()
        model_match = MODEL_NAME_PATTERN.search(text)
        if not model_match:
            continue
        model_name = model_match.group(1)
        connectors: Dict[str, str] = {}
        for conn_type, conn_name in CONNECTOR_PATTERN.findall(text):
            direction = "in" if conn_type == "RealInput" else "out"
            connectors[conn_name] = direction
        models[model_name] = connectors
    return models


def verify_interfaces(
    parts: Dict[str, List[Dict[str, str]]], models: Dict[str, Dict[str, str]]
) -> int:
    exit_code = 0
    common_parts = sorted(set(parts) & set(models))
    if not common_parts:
        print("No overlapping part/model names found.", file=sys.stderr)
        return 1

    for part_name in common_parts:
        arch_ports = {
            port["name"]: port
            for port in parts[part_name]
            if port["direction"] in {"in", "out"}
        }
        model_ports = models[part_name]

        missing = sorted(set(arch_ports) - set(model_ports))
        extra = sorted(set(model_ports) - set(arch_ports))
        mismatched = sorted(
            name
            for name in set(arch_ports) & set(model_ports)
            if arch_ports[name]["direction"] != model_ports[name]
        )

        if not missing and not extra and not mismatched:
            print(f"[OK]    {part_name}")
            continue

        exit_code = 2
        print(f"[WARN]  {part_name}")
        if missing:
            formatted = ", ".join(
                f"{name}({arch_ports[name]['direction']})" for name in missing
            )
            print(f"  - Missing in Modelica: {formatted}")
        if mismatched:
            formatted = ", ".join(
                f"{name} arch={arch_ports[name]['direction']} model={model_ports[name]}"
                for name in mismatched
            )
            print(f"  - Direction mismatch: {formatted}")
        if extra:
            formatted = ", ".join(
                f"{name}({model_ports[name]})" for name in extra
            )
            print(f"  - Extra connectors in Modelica: {formatted}")

    orphan_models = sorted(set(models) - set(parts))
    if orphan_models:
        print("\nModels with no matching part definition:", ", ".join(orphan_models))

    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify Modelica interfaces against the SysML architecture."
    )
    parser.add_argument(
        "--architecture",
        default="architecture/aircraft_architecture.sysml",
        type=Path,
        help="Path to the SysML architecture file.",
    )
    parser.add_argument(
        "--models-dir",
        default="models/WingmanDrone",
        type=Path,
        help="Directory containing Modelica models (*.mo).",
    )
    args = parser.parse_args()

    if not args.architecture.exists():
        print(f"Architecture file not found: {args.architecture}", file=sys.stderr)
        return 1
    if not args.models_dir.exists():
        print(f"Modelica directory not found: {args.models_dir}", file=sys.stderr)
        return 1

    parts = parse_architecture_parts(args.architecture)
    models = parse_modelica_connectors(args.models_dir)
    return verify_interfaces(parts, models)


if __name__ == "__main__":
    sys.exit(main())
