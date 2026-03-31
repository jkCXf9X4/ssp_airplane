"""Geospatial helpers shared by scenario generation and analysis."""

from .geometry import destination_point, haversine_distance_km, local_path_distance_km, project_waypoints_to_local_km

__all__ = [
    "destination_point",
    "haversine_distance_km",
    "local_path_distance_km",
    "project_waypoints_to_local_km",
]
