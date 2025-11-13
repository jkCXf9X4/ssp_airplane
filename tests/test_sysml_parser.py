from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from utils.sysmlv2_arch_parser import parse_sysml_folder  # type: ignore  # noqa: E402


def test_parser_collects_parts_and_ports():
    architecture = parse_sysml_folder(REPO_ROOT / "architecture")
    assert architecture.package == "WingmanDrone"
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
        conn.src_component == "MissionComputer"
        and conn.src_port == "flightStatus"
        and conn.dst_component == "AutopilotModule"
        and conn.dst_port == "feedbackBus"
        for conn in architecture.connections
    )
