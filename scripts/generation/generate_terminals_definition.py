#!/usr/bin/env python3
"""Create FMI terminals per FMU/component so variable names align with each modelDescription."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Iterable, Optional
import xml.etree.ElementTree as ET

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from scripts.utils.sysml_helpers import load_architecture
from scripts.utils.sysmlv2_arch_parser import (
    SysMLArchitecture,
    SysMLPartDefinition,
    SysMLPortDefinition,
)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "terminalsAndIcons.xml"


def _indent(tree: ET.ElementTree) -> None:
    ET.indent(tree, space="  ", level=0)


def _select_components(architecture: SysMLArchitecture, names: Optional[Iterable[str]]) -> list[SysMLPartDefinition]:
    if names:
        ordered: list[SysMLPartDefinition] = []
        seen: set[str] = set()
        for name in names:
            name = name.strip()
            if not name or name in seen or name not in architecture.parts:
                continue
            ordered.append(architecture.parts[name])
            seen.add(name)
        return ordered
    return [architecture.parts[name] for name in sorted(architecture.parts)]


def _member_entries(port_def: Optional[SysMLPortDefinition], port_name: str, port_doc: Optional[str]) -> list[tuple[str, str, Optional[str]]]:
    if not port_def or not port_def.attributes:
        return [(port_name, port_name, port_doc)]
    entries: list[tuple[str, str, Optional[str]]] = []
    for attr_name in sorted(port_def.attributes):
        attr = port_def.attributes[attr_name]
        variable_name = f"{port_name}.{attr.name}"
        entries.append((attr.name, variable_name, attr.doc))
    return entries


def build_terminals_tree(components: Iterable[SysMLPartDefinition]) -> ET.ElementTree:
    root = ET.Element("fmiTerminalsAndIcons", attrib={"fmiVersion": "3.0"})
    terminals_elem = ET.SubElement(root, "Terminals")

    for component in components:
        port_counters: Dict[str, int] = {}
        for port in component.ports:
            if not port.payload:
                continue
            counter = port_counters.get(port.name, 0) + 1
            port_counters[port.name] = counter
            terminal_name = f"{component.name}_{port.name}_{counter}"
            term_attrs = {
                "name": terminal_name,
                "matchingRule": "plug",
                "terminalKind": port.payload,
            }
            if port.doc:
                term_attrs["description"] = port.doc
            terminal_elem = ET.SubElement(terminals_elem, "Terminal", attrib=term_attrs)

            for member_name, variable_name, description in _member_entries(port.payload_def, port.name, port.doc):
                member_attrs = {
                    "variableKind": "signal",
                    "variableName": variable_name,
                    "memberName": member_name,
                }
                if description:
                    member_attrs["description"] = description
                ET.SubElement(terminal_elem, "TerminalMemberVariable", attrib=member_attrs)

    tree = ET.ElementTree(root)
    _indent(tree)
    return tree


def generate_terminals_file(
    architecture_path: Path,
    output_path: Path,
    components: Optional[Iterable[str]] = None,
) -> Path:
    architecture = load_architecture(architecture_path)
    targets = _select_components(architecture, components)
    tree = build_terminals_tree(targets)
    ensure_parent_dir(output_path)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return output_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Path to the SysML architecture directory or a file within it.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination path for the generated terminalsAndIcons.xml file.",
    )
    parser.add_argument(
        "--components",
        nargs="*",
        help="Optional subset of component names to include.",
    )
    args = parser.parse_args(argv)

    try:
        output_path = generate_terminals_file(args.architecture, args.output, args.components)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
