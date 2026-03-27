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
    binding_offset_expression,
    part_instance_fields,
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
        "#include <stddef.h>",
        "#include <stdint.h>",
        "",
        f"/* Generated from architecture package {architecture.package}. Do not edit manually. */",
        "",
        f"typedef enum {architecture.package}_ScalarType {{",
        f"  {architecture.package.upper()}_SCALAR_REAL = 0,",
        f"  {architecture.package.upper()}_SCALAR_INTEGER = 1,",
        f"  {architecture.package.upper()}_SCALAR_BOOLEAN = 2,",
        f"  {architecture.package.upper()}_SCALAR_STRING = 3,",
        f"}} {architecture.package}_ScalarType;",
        "",
        f"typedef struct {architecture.package}_FieldBinding {{",
        "  int value_reference;",
        f"  {architecture.package}_ScalarType scalar_type;",
        "  size_t offset;",
        "  bool writable;",
        f"}} {architecture.package}_FieldBinding;",
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

    lines.extend(
        [
            "#ifdef __cplusplus",
            '#include <string>',
            "",
        ]
    )

    for part_name, part in architecture.parts.items():
        if part_name == architecture.package:
            continue
        specs = part_specs[part_name]
        lines.append(f"struct {architecture.package}_{part_name}_Instance {{")
        for field_type, field_name, default_value in part_instance_fields(architecture.package, part):
            lines.append(f"  {field_type} {field_name} = {default_value};")
        lines.append("};")
        lines.append("")

        lines.append(
            f"inline constexpr {architecture.package}_FieldBinding {architecture.package}_{part_name}_Bindings[] = {{"
        )
        for spec in specs:
            scalar_name = f"{architecture.package.upper()}_SCALAR_{spec.fmi_type.upper()}"
            writable = "false" if spec.causality == "output" else "true"
            lines.append(
                "  "
                + "{"
                + f"{architecture.package.upper()}_{part_name.upper()}_VR_{sanitize_c_identifier(spec.name)}, "
                + f"{scalar_name}, "
                + f"{binding_offset_expression(architecture.package, part, spec)}, "
                + f"{writable}"
                + "},"
            )
        lines.append("};")
        lines.append(
            f"inline constexpr size_t {architecture.package}_{part_name}_BindingCount = "
            f"sizeof({architecture.package}_{part_name}_Bindings) / sizeof({architecture.package}_{part_name}_Bindings[0]);"
        )
        lines.append("")

    lines.append("#endif  /* __cplusplus */")

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
