from __future__ import annotations

import math

# Mirrors the Modelica navigation arithmetic in AutopilotModule.mo so we can sanity-check
# waypoint handling without rebuilding FMUs.
WAYPOINT_PROXIMITY_KM = 10.0
ALTITUDE_PROXIMITY_KM = 0.5
THRUST_TO_SPEED_GAIN = 4.0
CLIMB_BLEED_FRACTION = 0.35
MIN_AIRSPEED = 50.0
DEFAULT_THROTTLE = 0.7
TARGET_AIRSPEED = 220.0
AIRSPEED_THROTTLE_GAIN = 0.003
CLIMB_THROTTLE_GAIN = 0.01
MIN_THROTTLE = 0.2


def compute_heading_distance_xyz(
    current_x_km: float, current_y_km: float, current_z_km: float,
    target_x_km: float, target_y_km: float, target_z_km: float,
) -> tuple[float, float]:
    dx = target_x_km - current_x_km
    dy = target_y_km - current_y_km
    dz_km = target_z_km - current_z_km
    heading = math.degrees(math.atan2(dy, dx))
    distance_km = math.sqrt(dx**2 + dy**2 + dz_km**2)
    return heading, distance_km


def heading_error(target_heading: float, current_yaw: float) -> float:
    delta_rad = math.radians(target_heading - current_yaw)
    return math.degrees(math.atan2(math.sin(delta_rad), math.cos(delta_rad)))


def test_heading_and_distance_follow_trajectory():
    heading, distance = compute_heading_distance_xyz(0.0, 0.0, 0.0, 10.0, 15.0, 1.0)
    assert 50.0 < heading < 60.0  # northeast turn
    assert 18.0 < distance < 19.0
    err = heading_error(heading, current_yaw=10.0)
    assert 46.0 < err < 47.0  # turn toward target instead of wrapping long-way around


def test_heading_error_wraps_shortest_turn():
    err = heading_error(target_heading=350.0, current_yaw=10.0)
    assert -25.0 < err < -15.0  # chooses -20 deg, not +340 deg


def test_proximity_detection_threshold():
    _, distance = compute_heading_distance_xyz(1.0, 1.0, 0.5, 1.1, 1.0, 0.5)
    assert distance < WAYPOINT_PROXIMITY_KM


def has_arrived(current: tuple[float, float, float], target: tuple[float, float, float]) -> bool:
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    dz = target[2] - current[2]
    horizontal = math.hypot(dx, dy)
    vertical = abs(dz)
    return horizontal <= WAYPOINT_PROXIMITY_KM and vertical <= ALTITUDE_PROXIMITY_KM


def test_arrival_requires_altitude_match():
    assert not has_arrived((0.0, 0.0, 0.0), (5.0, 5.0, 2.0))
    assert has_arrived((0.0, 0.0, 0.0), (5.0, 5.0, 0.25))


def environment_speed(thrust_kn: float, pitch_deg: float) -> tuple[float, float]:
    base_speed = max(MIN_AIRSPEED, thrust_kn * THRUST_TO_SPEED_GAIN)
    bleed = max(0.5, 1 - CLIMB_BLEED_FRACTION * max(0.0, math.sin(math.radians(pitch_deg))))
    speed = max(MIN_AIRSPEED, base_speed * bleed)
    climb_rate = speed * math.sin(math.radians(pitch_deg))
    return speed, climb_rate


def autopilot_throttle_cmd(airspeed: float, climb_rate: float) -> float:
    throttle = DEFAULT_THROTTLE
    throttle += AIRSPEED_THROTTLE_GAIN * (TARGET_AIRSPEED - airspeed)
    throttle += CLIMB_THROTTLE_GAIN * max(0.0, climb_rate)
    return max(MIN_THROTTLE, min(1.0, throttle))


def test_climb_bleeds_speed_in_environment():
    level_speed, level_climb = environment_speed(thrust_kn=100.0, pitch_deg=0.0)
    climb_speed, climb_rate = environment_speed(thrust_kn=100.0, pitch_deg=20.0)
    assert level_speed > climb_speed
    assert level_climb == 0.0
    assert climb_rate > 0.0


def test_autopilot_adds_throttle_when_slow_and_climbing():
    throttle_level = autopilot_throttle_cmd(airspeed=TARGET_AIRSPEED, climb_rate=0.0)
    throttle_climb = autopilot_throttle_cmd(airspeed=TARGET_AIRSPEED - 30.0, climb_rate=25.0)
    assert throttle_climb > throttle_level
    assert throttle_climb > DEFAULT_THROTTLE
