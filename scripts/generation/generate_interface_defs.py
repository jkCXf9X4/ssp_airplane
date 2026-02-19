#!/usr/bin/env python3
"""Emit interface definitions for SysML data-def types as Modelica records."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Optional

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import (
    ARCHITECTURE_DIR,
    MODELS_DIR,
    PACKAGE_NAME,
    ensure_parent_dir,
)

from pycps_sysmlv2 import SysMLPortDefinition, load_architecture

from scripts.common.modelica import map_modelica_type


DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT_PATH = MODELS_DIR / PACKAGE_NAME / "GeneratedInterfaces.mo"


def generate_modelica_package(ports: Dict[str, SysMLPortDefinition]) -> str:
    lines = [f"within {PACKAGE_NAME};", "package GeneratedInterfaces"]

    for port_name, port in sorted(ports.items()):
        if not port.attributes:
            continue

        lines.append(f"  connector {port_name}")
        for variable in port.attributes.values():
            mo_type = map_modelica_type(variable.type.as_string())
            lines.append(f"    {mo_type} {variable.name};")
        lines.append(f"  end {port_name};\n")

    lines.append("end GeneratedInterfaces;")
    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=DEFAULT_ARCH_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args(argv)

    architecture = load_architecture(args.architecture)
    port_definitions = architecture.port_definitions

    if not port_definitions:
        raise SystemExit("No data definitions found; nothing to generate.")

    ensure_parent_dir(args.output)
    content = generate_modelica_package(port_definitions)

    args.output.write_text(content, encoding="utf-8")
    print(f"Wrote Modelica interfaces to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
