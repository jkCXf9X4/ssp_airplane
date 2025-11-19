from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.utils.sysmlv2_arch_parser import parse_sysml_folder  # type: ignore  # noqa: E402


def test_parser_collects_parts_and_ports():
    architecture = parse_sysml_folder(REPO_ROOT / "architecture")
    assert architecture.package == "Aircraft"
    assert "MissionComputer" in architecture.parts

    mission_computer = architecture.part("MissionComputer")
    manual_input = next(port for port in mission_computer.ports if port.name == "manualInput")
    assert manual_input.direction == "in"
    assert manual_input.payload == "PilotCommand"
    assert manual_input.payload_def is not None
    assert "throttle_norm" in manual_input.payload_def.attributes

    pilot_command = architecture.port("PilotCommand")
    assert "hat_x" in pilot_command.attributes
    assert pilot_command.attributes["hat_x"].type == "Integer"



def test_connections_are_parsed():
    architecture = parse_sysml_folder(REPO_ROOT / "architecture")
    assert any(
        conn.src_component == "Environment"
        and conn.src_port == "flight_status"
        and conn.dst_component == "AutopilotModule"
        and conn.dst_port == "feedbackBus"
        for conn in architecture.connections
    )
