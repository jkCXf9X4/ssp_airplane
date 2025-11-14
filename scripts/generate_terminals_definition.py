#!/usr/bin/env python3
"""Create an FMI terminals definition (fmiTerminalsAndIcons) from the SysML architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional
import xml.etree.ElementTree as ET

from utils.sysmlv2_arch_parser import SysMLArchitecture, SysMLPortDefinition, parse_sysml_folder

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCH_PATH = REPO_ROOT / "architecture"
DEFAULT_OUTPUT = REPO_ROOT / "generated" / "terminalsAndIcons.xml"


def _indent(tree: ET.ElementTree) -> None:
    ET.indent(tree, space="  ", level=0)


def _select_port_definitions(architecture: SysMLArchitecture, names: Optional[Iterable[str]]) -> list[SysMLPortDefinition]:
    if names:
        ordered: list[SysMLPortDefinition] = []
        seen: set[str] = set()
        for name in names:
            name = name.strip()
            if not name or name in seen or name not in architecture.port_definitions:
                continue
            ordered.append(architecture.port_definitions[name])
            seen.add(name)
        return ordered
    return [architecture.port_definitions[name] for name in sorted(architecture.port_definitions)]


def _member_entries(port: SysMLPortDefinition) -> list[tuple[str, str, Optional[str]]]:
    if not port.attributes:
        return [("value", port.name, port.doc)]
    entries: list[tuple[str, str, Optional[str]]] = []
    for attr_name in sorted(port.attributes):
        attr = port.attributes[attr_name]
        entries.append((attr.name, f"{port.name}.{attr.name}", attr.doc))
    return entries


def build_terminals_tree(port_defs: Iterable[SysMLPortDefinition]) -> ET.ElementTree:
    root = ET.Element("fmiTerminalsAndIcons", attrib={"fmiVersion": "3.0"})
    terminals_elem = ET.SubElement(root, "Terminals")

    for port in port_defs:
        term_attrs = {"name": port.name, "matchingRule": "plug"}
        if port.doc:
            term_attrs["description"] = port.doc
        terminal_elem = ET.SubElement(terminals_elem, "Terminal", attrib=term_attrs)

        for member_name, variable_name, description in _member_entries(port):
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
    port_names: Optional[Iterable[str]] = None,
) -> Path:
    if architecture_path.is_file():
        architecture_path = architecture_path.parent
    architecture = parse_sysml_folder(architecture_path)
    targets = _select_port_definitions(architecture, port_names)
    tree = build_terminals_tree(targets)
    output_path.parent.mkdir(parents=True, exist_ok=True)
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
        "--ports",
        nargs="*",
        help="Optional subset of port definition names to include.",
    )
    args = parser.parse_args(argv)

    try:
        output_path = generate_terminals_file(args.architecture, args.output, args.ports)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
