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


def _cpp_type_tag(package: str, fmi_type: str) -> str:
    return f"{package.upper()}_DATA_{fmi_type.upper()}"


def _member_access(path: str) -> str:
    return ".".join(path.split("."))


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
    ]

    for port_name, port_def in architecture.port_definitions.items():
        lines.append(f"typedef struct {package}_{port_name} {{")
        for field_name, field_type in port_struct_fields(port_def):
            lines.append(f"  {field_type} {field_name};")
        lines.append(f"}} {package}_{port_name};")
        lines.append("")

    lines.extend(
        [
            "#ifdef __cplusplus",
            "#include <string>",
            "",
            f"enum {package}_DataType {{",
            f"  {package.upper()}_DATA_NONE = 0,",
            f"  {package.upper()}_DATA_REAL = 1,",
            f"  {package.upper()}_DATA_INTEGER = 2,",
            f"  {package.upper()}_DATA_BOOLEAN = 3,",
            f"  {package.upper()}_DATA_STRING = 4,",
            f"}};",
            "",
            f"struct {package}_VrMapping {{",
            "  void* data = nullptr;",
            f"  {package}_DataType type = {package.upper()}_DATA_NONE;",
            "  bool writable = false;",
            "};",
            "#endif  /* __cplusplus */",
            "",
        ]
    )
    return lines


def _part_header_lines(package: str, part_name: str, part, specs: list) -> list[str]:
    vr_count = len(specs)
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
            f"inline constexpr size_t {package}_{part_name}_VrCount = {vr_count};",
            "",
            f"struct {package}_{part_name}_Instance {{",
            f"  {package}_VrMapping vr_map[{vr_count}] = {{}};",
        ]
    )
    for field_type, field_name, default_value in part_instance_fields(package, part):
        lines.append(f"  {field_type} {field_name} = {default_value};")
    lines.extend(["};", ""])

    lines.append(
        f"inline void {package}_{part_name}_initialize_vr_map({package}_{part_name}_Instance* instance) {{"
    )
    lines.append(f"  for (size_t i = 0; i < {package}_{part_name}_VrCount; ++i) {{")
    lines.append(f"    instance->vr_map[i] = {{nullptr, {package.upper()}_DATA_NONE, false}};")
    lines.append("  }")
    for spec in specs:
        writable = "false" if spec.causality == "output" else "true"
        lines.append(
            f"  instance->vr_map[{package.upper()}_{part_name.upper()}_VR_{sanitize_c_identifier(spec.name)}] = "
            + "{"
            + f"&instance->{_member_access(spec.field_path)}, "
            + f"{_cpp_type_tag(package, spec.fmi_type)}, "
            + f"{writable}"
            + "};"
        )
    lines.extend(["}", "", "#endif  /* __cplusplus */"])
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
