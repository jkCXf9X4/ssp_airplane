"""Generate Modelica interface definitions from SysML data definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from pycps_sysmlv2 import NodeType, SysMLParser, SysMLPortDefinition

from scripts.lib.paths import ARCHITECTURE_DIR, GENERATED_MODELICA_INTERFACE_FILE, ensure_parent_dir
from scripts.lib.common.sysml import modelica_connector_type

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT_PATH = GENERATED_MODELICA_INTERFACE_FILE


def generate_modelica_package(ports: Dict[str, SysMLPortDefinition]) -> str:
    lines = ["within AircraftCommon;", "package GeneratedInterfaces"]
    for port_name, port in sorted(ports.items()):
        attributes = port.defs(NodeType.Attribute)
        if not attributes:
            continue

        lines.append(f"  connector {port_name}")
        for variable in attributes.values():
            type_name = variable.type.as_string()
            mo_type = modelica_connector_type(type_name)
            lines.append(f"    {mo_type} {variable.name};")
        lines.append(f"  end {port_name};\n")

    lines.append("end GeneratedInterfaces;")
    return "\n".join(lines)


def write_modelica_interfaces(
    architecture_path: Path = DEFAULT_ARCH_PATH,
    output: Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    architecture = SysMLParser(architecture_path).parse()
    port_definitions = architecture.port_definitions

    if not port_definitions:
        raise SystemExit("No data definitions found; nothing to generate.")

    ensure_parent_dir(output)
    content = generate_modelica_package(port_definitions)
    output.write_text(content, encoding="utf-8")
    return output
