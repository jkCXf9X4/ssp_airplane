from __future__ import annotations

import sys
from pathlib import Path

import pycps_sysml2

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _architecture():
    return pycps_sysml2.load(REPO_ROOT / "architecture")


def test_parser_collects_parts_and_ports():
    architecture = _architecture()
    assert architecture.package_name == "Aircraft"
    assert "MissionComputer" in architecture.part_definitions

    mission_computer = architecture.part_definitions["MissionComputer"]
    manual_input = mission_computer.ports["manualInput"]
    assert manual_input.direction == "in"
    assert manual_input.type_name == "PilotCommand"

    pilot_command = architecture.port_definitions["PilotCommand"]
    assert "throttle_norm" in pilot_command.attributes
    assert pilot_command.attributes["hat_x"].type_name == "Integer"


def test_connections_are_parsed():
    architecture = _architecture()
    aircraft_model = architecture.part_definitions["AircraftModel"]
    assert any(
        conn.source_part == "environment"
        and conn.source_port == "flight_status"
        and conn.destination_part == "autopilot_module"
        and conn.destination_port == "feedbackBus"
        for conn in aircraft_model.connections.values()
    )
