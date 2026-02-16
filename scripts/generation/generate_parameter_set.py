#!/usr/bin/env python3
"""Generate an SSP parameter set (SSV) from architecture attributes."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pyssp_standard.ssv import SSV
from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from pycps_sysmlv2 import SysMLArchitecture, SysMLAttribute, SysMLPartDefinition, load_architecture
from pycps_sysmlv2.type_utils import infer_primitive
from scripts.utils.sysml_compat import composition_components, literal_value

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT = GENERATED_DIR / "parameters.ssv"


def _normalize_type(attr: SysMLAttribute) -> str:
    literal = literal_value(attr.value)
    return infer_primitive(attr.type, literal)


def _format_value(tag: str, literal):
    if literal is None:
        return ""
    if tag == "Boolean":
        return "true" if bool(literal) else "false"
    if tag == "Integer":
        return int(literal)
    if tag == "Real":
        return f"{float(literal):g}"
    return str(literal)


def _parameter_entries(architecture: SysMLArchitecture, components: Optional[Iterable[str]]) -> list[tuple[str, SysMLAttribute]]:
    component_pairs = composition_components(architecture)
    selected: list[tuple[str, SysMLPartDefinition]] = []
    if components:
        requested = {name.strip() for name in components if name.strip()}
        for instance_name, part in component_pairs:
            if instance_name in requested or part.name in requested:
                selected.append((instance_name, part))
    else:
        selected = component_pairs

    entries: list[tuple[str, SysMLAttribute]] = []
    for instance_name, part in selected:
        for attr_name in sorted(part.attributes):
            attr = part.attributes[attr_name]
            full_name = f"{instance_name}.{attr.name}"
            entries.append((full_name, attr))
    return entries


def _populate_parameter_set(ssv: SSV, parameter_pairs: Iterable[tuple[str, SysMLAttribute]]) -> None:
    for name, attr in parameter_pairs:
        literal = literal_value(attr.value)
        if isinstance(literal, (list, tuple)):
            sample = next((item for item in literal if item is not None), None)
            data_type = infer_primitive(attr.type, sample)
            for idx, item in enumerate(literal, start=1):
                indexed_name = f"{name}[{idx}]"
                formatted = _format_value(data_type, item)
                ssv.add_parameter(indexed_name, ptype=data_type, value=formatted)
            continue

        data_type = _normalize_type(attr)
        formatted = _format_value(data_type, literal)
        ssv.add_parameter(name, ptype=data_type, value=formatted)


def _strip_none_parameter_attrs(ssv: SSV) -> None:
    for parameter in ssv.parameters:
        type_value = parameter["type_value"]
        type_value.parameter = {
            key: value
            for key, value in type_value.parameter.items()
            if value is not None
        }


def generate_parameter_set(
    architecture_path: Path,
    output_path: Path,
    components: Optional[Iterable[str]] = None,
) -> Path:
    architecture = load_architecture(architecture_path)
    pairs = _parameter_entries(architecture, components)
    ensure_parent_dir(output_path)
    with SSV(output_path, mode="w", name="ArchitecturalDefaults") as ssv:
        _populate_parameter_set(ssv, pairs)
        _strip_none_parameter_attrs(ssv)
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
