#!/usr/bin/env python3
"""Export architecture-derived C headers for native component implementations."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_parent_dir
from scripts.utils.c_interface_export import (
    architecture_part_specs,
    c_primitive,
    port_struct_fields,
    sanitize_c_identifier,
)
from scripts.utils.sysml_helpers import load_architecture

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT_PATH = GENERATED_DIR / "architecture_interface.h"


def generate_header(source: Path, output: Path) -> Path:
    architecture = load_architecture(source)
    part_specs = architecture_part_specs(architecture)

    lines = [
        "#pragma once",
        "",
        "#include <stdbool.h>",
        "#include <stdint.h>",
        "",
        f"/* Generated from architecture package {architecture.package}. Do not edit manually. */",
        "",
    ]

    for port_name, port_def in architecture.port_definitions.items():
        lines.append(f"typedef struct {architecture.package}_{port_name} {{")
        for field_name, field_type in port_struct_fields(port_def):
            lines.append(f"  {field_type} {field_name};")
        lines.append(f"}} {architecture.package}_{port_name};")
        lines.append("")

    for part_name, specs in part_specs.items():
        if part_name == architecture.package:
            continue
        lines.append(f"typedef enum {architecture.package}_{part_name}_ValueReference {{")
        for spec in specs:
            enum_name = sanitize_c_identifier(spec.name)
            lines.append(
                f"  {architecture.package.upper()}_{part_name.upper()}_VR_{enum_name} = {spec.value_reference},"
            )
        lines.append(f"}} {architecture.package}_{part_name}_ValueReference;")
        lines.append("")

    ensure_parent_dir(output)
    output.write_text("\n".join(lines))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=DEFAULT_ARCH_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    path = generate_header(args.architecture, args.output)
    print(f"Wrote C interface header to {path}")


if __name__ == "__main__":
    main()
