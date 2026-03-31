"""Geospatial helper utilities for waypoint generation and simulation."""
from __future__ import annotations

import math
from typing import Dict, List

EARTH_RADIUS_KM = 6371.0


def haversine_distance_km(points: List[Dict[str, float]]) -> float:
    """Compute total surface distance of consecutive latitude/longitude points."""
    total = 0.0
    for i in range(len(points) - 1):
        lat1 = math.radians(float(points[i]["latitude_deg"]))
        lon1 = math.radians(float(points[i]["longitude_deg"]))
        lat2 = math.radians(float(points[i + 1]["latitude_deg"]))
        lon2 = math.radians(float(points[i + 1]["longitude_deg"]))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        h = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        total += 2 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(h)))
    return total


def destination_point(
    latitude_deg: float, longitude_deg: float, distance_km: float, bearing_rad: float
) -> Dict[str, float]:
    """Compute the destination geodetic point from a start, distance, and bearing."""
    lat1 = math.radians(latitude_deg)
    lon1 = math.radians(longitude_deg)
    ang_dist = distance_km / EARTH_RADIUS_KM
    sin_lat2 = (
        math.sin(lat1) * math.cos(ang_dist)
        + math.cos(lat1) * math.sin(ang_dist) * math.cos(bearing_rad)
    )
    lat2 = math.asin(max(-1.0, min(1.0, sin_lat2)))
    y = math.sin(bearing_rad) * math.sin(ang_dist) * math.cos(lat1)
    x = math.cos(ang_dist) - math.sin(lat1) * math.sin(lat2)
    lon2 = lon1 + math.atan2(y, x)
    lon2 = (lon2 + math.pi) % (2 * math.pi) - math.pi
    return {
        "latitude_deg": math.degrees(lat2),
        "longitude_deg": math.degrees(lon2),
    }


def project_waypoints_to_local_km(points: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """Convert geodetic latitude/longitude/altitude to a local X/Y/Z frame in km."""
    if not points:
        return []
    origin = points[0]
    lat0 = float(origin["latitude_deg"])
    lon0 = float(origin["longitude_deg"])
    lat0_rad = math.radians(lat0)
    projected: List[Dict[str, float]] = []
    for point in points:
        lat = float(point["latitude_deg"])
        lon = float(point["longitude_deg"])
        alt_m = float(point.get("altitude_m", 0.0))
        x_km = 111.0 * (lat - lat0)
        y_km = 111.0 * math.cos(lat0_rad) * (lon - lon0)
        projected.append({"x_km": x_km, "y_km": y_km, "z_km": alt_m / 1000.0})
    return projected


def local_path_distance_km(points: List[Dict[str, float]]) -> float:
    """Compute cumulative straight-line distance between local XYZ points."""
    total = 0.0
    for i in range(len(points) - 1):
        dx = points[i + 1]["x_km"] - points[i]["x_km"]
        dy = points[i + 1]["y_km"] - points[i]["y_km"]
        dz = points[i + 1].get("z_km", 0.0) - points[i].get("z_km", 0.0)
        total += math.sqrt(dx * dx + dy * dy + dz * dz)
    return total
