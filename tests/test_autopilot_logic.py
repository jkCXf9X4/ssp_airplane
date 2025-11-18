from __future__ import annotations

import math

# Mirrors the Modelica navigation arithmetic in AutopilotModule.mo so we can sanity-check
# waypoint handling without rebuilding FMUs.
WAYPOINT_PROXIMITY_KM = 10.0


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
