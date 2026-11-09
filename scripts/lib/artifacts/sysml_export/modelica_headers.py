"""Generate Modelica interface definitions from SysML data definitions.

Rebased on ``pycps_sml2``. Divergence: the airplane models pin the
``AircraftCommon.GeneratedInterfaces`` package layout, so this emitter stays
here instead of adopting ``pyfmi_sml2.modelica`` (whose package layout differs).
"""
from __future__ import annotations

from pycps_sysml2 import Architecture

#: Port definitions that specialize this marker are FMU parameter surfaces and
#: never become Modelica connectors (the models reference data ports only).
_PARAMETER_INTERFACE_MARKER = "ParameterInterface"


def generate_modelica_package(architecture: Architecture) -> str:
    """A ``package GeneratedInterfaces`` with one connector per data port."""
    lines = ["within AircraftCommon;", "package GeneratedInterfaces"]
    for port_name, port in sorted(architecture.port_definitions.items()):
        if _PARAMETER_INTERFACE_MARKER in port.specializes:
            continue
        if not port.attributes:
            continue
        lines.append(f"  connector {port_name}")
        for attribute in port.attributes.values():
            lines.append(f"    {attribute.primitive_type_str()} {attribute.name};")
        lines.append(f"  end {port_name};\n")
    lines.append("end GeneratedInterfaces;")
    return "\n".join(lines)