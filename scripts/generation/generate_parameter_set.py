#!/usr/bin/env python3
"""Generate an SSP parameter set (SSV) from architecture attributes."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional
import xml.etree.ElementTree as ET

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from scripts.common.sysml_values import parse_literal
from scripts.utils.sysml_helpers import load_architecture
from scripts.utils.sysmlv2_arch_parser import SysMLArchitecture, SysMLAttribute
from scripts.utils.type_utils import infer_primitive

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "parameters.ssv"

SSV_NAMESPACE = "http://ssp-standard.org/SSP1/ParameterValues"

ET.register_namespace("ssv", SSV_NAMESPACE)


def _normalize_type(attr: SysMLAttribute) -> str:
    literal = parse_literal(attr.value)
    return infer_primitive(attr.type, literal)


def _format_value(tag: str, literal) -> str:
    if literal is None:
        return ""
    if tag == "Boolean":
        return "true" if bool(literal) else "false"
    if tag == "Integer":
        return str(int(literal))
    if tag == "Real":
        return f"{float(literal):g}"
    return str(literal)


def _parameter_entries(architecture: SysMLArchitecture, components: Optional[Iterable[str]]) -> list[tuple[str, SysMLAttribute]]:
    parts = architecture.parts
    selected = (
        [parts[name] for name in components if name in parts]
        if components
        else [parts[name] for name in sorted(parts)]
    )
    entries: list[tuple[str, SysMLAttribute]] = []
    for part in selected:
        for attr_name in sorted(part.attributes):
            attr = part.attributes[attr_name]
            full_name = f"{part.name}.{attr.name}"
            entries.append((full_name, attr))
    return entries


def build_parameter_tree(parameter_pairs: Iterable[tuple[str, SysMLAttribute]]) -> ET.ElementTree:
    root = ET.Element(f"{{{SSV_NAMESPACE}}}ParameterSet", attrib={"name": "ArchitecturalDefaults", "version": "1.0"})
    params_elem = ET.SubElement(root, f"{{{SSV_NAMESPACE}}}Parameters")

    for name, attr in parameter_pairs:
        literal = parse_literal(attr.value)
        data_type = _normalize_type(attr)
        param_elem = ET.SubElement(params_elem, f"{{{SSV_NAMESPACE}}}Parameter", attrib={"name": name})
        value_elem = ET.SubElement(param_elem, f"{{{SSV_NAMESPACE}}}{data_type}")
        formatted = _format_value(data_type, literal)
        if formatted:
            value_elem.set("value", formatted)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    return tree


def generate_parameter_set(
    architecture_path: Path,
    output_path: Path,
    components: Optional[Iterable[str]] = None,
) -> Path:
    architecture = load_architecture(architecture_path)
    pairs = _parameter_entries(architecture, components)
    tree = build_parameter_tree(pairs)
    ensure_parent_dir(output_path)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return output_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Path to the SysML architecture directory or a file inside it.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination for the generated .ssv file.",
    )
    parser.add_argument(
        "--components",
        nargs="*",
        help="Optional subset of component names to include.",
    )
    args = parser.parse_args(argv)

    try:
        output_path = generate_parameter_set(args.architecture, args.output, args.components)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
