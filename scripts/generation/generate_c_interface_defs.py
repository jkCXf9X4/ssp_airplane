#!/usr/bin/env python3
"""Export architecture-derived C/C++ headers for native component implementations."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, GENERATED_DIR, ensure_directory
from scripts.utils.c_interface_export import (
    architecture_part_specs,
    binding_offset_expression,
    part_instance_fields,
    port_struct_fields,
    sanitize_c_identifier,
)
from scripts.utils.sysml_helpers import load_architecture

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT_DIR = GENERATED_DIR / "interfaces"


def common_header_name(package: str) -> str:
    return f"{package}_InterfaceCommon.h"


def part_header_name(package: str, part_name: str) -> str:
    return f"{package}_{part_name}.h"


def _common_header_lines(package: str, architecture) -> list[str]:
    lines = [
        "#pragma once",
        "",
        "#include <stdbool.h>",
        "#include <stddef.h>",
        "#include <stdint.h>",
        "",
        f"/* Generated from architecture package {package}. Do not edit manually. */",
        "",
        f"typedef enum {package}_ScalarType {{",
        f"  {package.upper()}_SCALAR_REAL = 0,",
        f"  {package.upper()}_SCALAR_INTEGER = 1,",
        f"  {package.upper()}_SCALAR_BOOLEAN = 2,",
        f"  {package.upper()}_SCALAR_STRING = 3,",
        f"}} {package}_ScalarType;",
        "",
        f"typedef struct {package}_FieldBinding {{",
        "  int value_reference;",
        f"  {package}_ScalarType scalar_type;",
        "  size_t offset;",
        "  bool writable;",
        f"}} {package}_FieldBinding;",
        "",
        "#ifdef __cplusplus",
        "#include <string>",
        "",
        f"typedef const std::string& (*{package}_StringFieldGetter)(const void* instance);",
        f"typedef std::string& (*{package}_StringFieldGetterMut)(void* instance);",
        "",
        f"typedef struct {package}_StringFieldBinding {{",
        "  int value_reference;",
        f"  {package}_StringFieldGetter get;",
        f"  {package}_StringFieldGetterMut get_mut;",
        "  bool writable;",
        f"}} {package}_StringFieldBinding;",
        "#endif  /* __cplusplus */",
        "",
    ]

    for port_name, port_def in architecture.port_definitions.items():
        lines.append(f"typedef struct {package}_{port_name} {{")
        for field_name, field_type in port_struct_fields(port_def):
            lines.append(f"  {field_type} {field_name};")
        lines.append(f"}} {package}_{port_name};")
        lines.append("")

    return lines


def _part_header_lines(package: str, part_name: str, part, specs: list) -> list[str]:
    lines = [
        "#pragma once",
        "",
        f'#include "{common_header_name(package)}"',
        "",
        f"/* Generated interface for {package}.{part_name}. Do not edit manually. */",
        "",
        f"typedef enum {package}_{part_name}_ValueReference {{",
    ]
    for spec in specs:
        lines.append(
            f"  {package.upper()}_{part_name.upper()}_VR_{sanitize_c_identifier(spec.name)} = {spec.value_reference},"
        )
    lines.extend(
        [
            f"}} {package}_{part_name}_ValueReference;",
            "",
            "#ifdef __cplusplus",
            "",
            f"struct {package}_{part_name}_Instance {{",
        ]
    )
    for field_type, field_name, default_value in part_instance_fields(package, part):
        lines.append(f"  {field_type} {field_name} = {default_value};")
    lines.extend(["};", ""])

    string_specs = [spec for spec in specs if spec.fmi_type == "String"]
    pod_specs = [spec for spec in specs if spec.fmi_type != "String"]

    for spec in string_specs:
        accessor_name = f"{package}_{part_name}_{sanitize_c_identifier(spec.name)}"
        lines.append(
            f"inline const std::string& {accessor_name}_get(const void* instance) {{ "
            f"return static_cast<const {package}_{part_name}_Instance*>(instance)->{spec.field_path}; }}"
        )
        lines.append(
            f"inline std::string& {accessor_name}_get_mut(void* instance) {{ "
            f"return static_cast<{package}_{part_name}_Instance*>(instance)->{spec.field_path}; }}"
        )
    if string_specs:
        lines.append("")

    if pod_specs:
        lines.append(f"inline constexpr {package}_FieldBinding {package}_{part_name}_Bindings[] = {{")
        for spec in pod_specs:
            writable = "false" if spec.causality == "output" else "true"
            lines.append(
                "  "
                + "{"
                + f"{package.upper()}_{part_name.upper()}_VR_{sanitize_c_identifier(spec.name)}, "
                + f"{package.upper()}_SCALAR_{spec.fmi_type.upper()}, "
                + f"{binding_offset_expression(package, part, spec)}, "
                + f"{writable}"
                + "},"
            )
        lines.append("};")
        lines.append(
            f"inline constexpr size_t {package}_{part_name}_BindingCount = "
            f"sizeof({package}_{part_name}_Bindings) / sizeof({package}_{part_name}_Bindings[0]);"
        )
    else:
        lines.append(f"inline constexpr const {package}_FieldBinding* {package}_{part_name}_Bindings = nullptr;")
        lines.append(f"inline constexpr size_t {package}_{part_name}_BindingCount = 0;")
    lines.append("")

    if string_specs:
        lines.append(
            f"inline constexpr {package}_StringFieldBinding {package}_{part_name}_StringBindings[] = {{"
        )
        for spec in string_specs:
            accessor_name = f"{package}_{part_name}_{sanitize_c_identifier(spec.name)}"
            writable = "false" if spec.causality == "output" else "true"
            lines.append(
                "  "
                + "{"
                + f"{package.upper()}_{part_name.upper()}_VR_{sanitize_c_identifier(spec.name)}, "
                + f"&{accessor_name}_get, "
                + f"&{accessor_name}_get_mut, "
                + f"{writable}"
                + "},"
            )
        lines.append("};")
        lines.append(
            f"inline constexpr size_t {package}_{part_name}_StringBindingCount = "
            f"sizeof({package}_{part_name}_StringBindings) / sizeof({package}_{part_name}_StringBindings[0]);"
        )
    else:
        lines.append(
            f"inline constexpr const {package}_StringFieldBinding* {package}_{part_name}_StringBindings = nullptr;"
        )
        lines.append(f"inline constexpr size_t {package}_{part_name}_StringBindingCount = 0;")
    lines.extend(["", "#endif  /* __cplusplus */"])
    return lines


def generate_headers(source: Path, output_dir: Path) -> list[Path]:
    architecture = load_architecture(source)
    part_specs = architecture_part_specs(architecture)

    ensure_directory(output_dir)
    written: list[Path] = []

    common_path = output_dir / common_header_name(architecture.package)
    common_path.write_text("\n".join(_common_header_lines(architecture.package, architecture)))
    written.append(common_path)

    for part_name, part in architecture.parts.items():
        if part_name == architecture.package:
            continue
        path = output_dir / part_header_name(architecture.package, part_name)
        path.write_text("\n".join(_part_header_lines(architecture.package, part_name, part, part_specs[part_name])))
        written.append(path)

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=DEFAULT_ARCH_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    written = generate_headers(args.architecture, args.output_dir)
    print(f"Wrote {len(written)} interface headers to {args.output_dir}")


if __name__ == "__main__":
    main()
