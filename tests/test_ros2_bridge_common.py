from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_TOP = Path(__file__).resolve().parents[3]
if str(REPO_TOP) not in sys.path:
    sys.path.insert(0, str(REPO_TOP))

from ros2_bridge.common import encode_control_packet, load_local_waypoints, parse_state_packet  # noqa: E402


def test_parse_state_packet_converts_local_km_to_meters() -> None:
    packet = parse_state_packet(
        json.dumps(
            {
                "transport": "Ros2UdpBridge",
                "reference_latitude_deg": 57.7,
                "reference_longitude_deg": 11.95,
                "reference_altitude_m": 12.0,
                "state": {"x_km": 1.5, "y_km": -2.0, "z_km": 0.75},
                "orientation": {"roll_deg": 1.0, "pitch_deg": 2.0, "yaw_deg": 3.0},
                "flight_status": {
                    "airspeed_mps": 250.0,
                    "energy_state_norm": 0.8,
                    "angle_of_attack_deg": 4.5,
                    "climb_rate": 12.0,
                    "health_code": 2,
                },
                "mission_status": {
                    "waypoint_index": 2,
                    "total_waypoints": 5,
                    "distance_to_waypoint_km": 42.0,
                    "arrived": False,
                    "complete": False,
                },
            }
        )
    )

    assert packet["state_m"] == {"x": 1500.0, "y": -2000.0, "z": 750.0}
    assert packet["mission_status"]["waypoint_index"] == 2


def test_encode_control_packet_emits_json_with_defaults() -> None:
    payload = encode_control_packet({"stick_pitch_norm": 0.2, "throttle_norm": 0.7})
    decoded = json.loads(payload.decode("utf-8"))

    assert decoded["stick_pitch_norm"] == 0.2
    assert decoded["throttle_norm"] == 0.7
    assert decoded["throttle_aux_norm"] == 0.7
    assert decoded["mode_switch"] == 0


def test_load_local_waypoints_projects_from_scenario_file(tmp_path: Path) -> None:
    scenario = tmp_path / "scenario.json"
    scenario.write_text(
        json.dumps(
            {
                "points": [
                    {"latitude_deg": 57.7, "longitude_deg": 11.95, "altitude_m": 12.0},
                    {"latitude_deg": 57.8, "longitude_deg": 12.05, "altitude_m": 1012.0},
                ]
            }
        ),
        encoding="utf-8",
    )

    waypoints = load_local_waypoints(scenario)
    assert waypoints[0] == {"x_km": 0.0, "y_km": 0.0, "z_km": 0.012}
    assert waypoints[1]["x_km"] > 0.0
    assert waypoints[1]["y_km"] > 0.0
