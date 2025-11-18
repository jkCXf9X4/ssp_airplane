from __future__ import annotations

import math

# Mirrors the Modelica navigation arithmetic in AutopilotModule.mo so we can sanity-check
# waypoint handling without rebuilding FMUs.
EARTH_KM_PER_DEG = 111.0
WAYPOINT_PROXIMITY_KM = 10.0


def compute_heading_distance(
    current_lat: float, current_lon: float, target_lat: float, target_lon: float
) -> tuple[float, float]:
    lat_rad = math.radians(current_lat)
    delta_lat = target_lat - current_lat
    delta_lon = target_lon - current_lon
    heading = math.degrees(
        math.atan2(math.cos(lat_rad) * delta_lon, delta_lat)
    )
    distance_km = EARTH_KM_PER_DEG * math.sqrt(
        delta_lat**2 + (math.cos(lat_rad) * delta_lon) ** 2
    )
    return heading, distance_km


def heading_error(target_heading: float, current_yaw: float) -> float:
    delta_rad = math.radians(target_heading - current_yaw)
    return math.degrees(math.atan2(math.sin(delta_rad), math.cos(delta_rad)))


def test_heading_and_distance_follow_trajectory():
    heading, distance = compute_heading_distance(45.0, 7.0, 45.1, 7.2)
    assert 50.0 < heading < 60.0  # northeast turn
    assert 19.0 < distance < 19.5
    err = heading_error(heading, current_yaw=10.0)
    assert 44.0 < err < 45.0  # turn toward target instead of wrapping long-way around


def test_heading_error_wraps_shortest_turn():
    err = heading_error(target_heading=350.0, current_yaw=10.0)
    assert -25.0 < err < -15.0  # chooses -20 deg, not +340 deg


def test_proximity_detection_threshold():
    _, distance = compute_heading_distance(10.0, 10.0, 10.05, 10.0)
    assert distance < WAYPOINT_PROXIMITY_KM
