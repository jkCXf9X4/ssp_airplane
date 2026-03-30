from __future__ import annotations

import sys
from pathlib import Path

from pycps_sysmlv2 import NodeType, SysMLParser

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def test_parser_collects_parts_and_ports():
    architecture = SysMLParser(REPO_ROOT / "architecture").parse()
    assert architecture.package == "Aircraft"
    assert "MissionComputer" in architecture.part_definitions

    mission_computer = architecture.part_definitions["MissionComputer"]
    manual_input = mission_computer.refs(NodeType.Port)["manualInput"]
    assert manual_input.direction == "in"
    assert manual_input.type == "PilotCommand"
    assert manual_input.ref_node is not None
    assert "throttle_norm" in manual_input.ref_node.defs(NodeType.Attribute)

    pilot_command = architecture.port_definitions["PilotCommand"]
    assert "hat_x" in pilot_command.defs(NodeType.Attribute)
    assert pilot_command.defs(NodeType.Attribute)["hat_x"].type.as_string() == "Integer"



def test_connections_are_parsed():
    architecture = SysMLParser(REPO_ROOT / "architecture").parse()
    system = architecture.get_def(NodeType.Part, "AircraftComposition")
    assert any(
        conn.src_part_node.ref_node.name == "Environment"
        and conn.src_port == "flight_status"
        and conn.dst_part_node.ref_node.name == "AutopilotModule"
        and conn.dst_port == "feedbackBus"
        for conn in system.defs(NodeType.Connection).values()
    )
