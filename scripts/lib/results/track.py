"""Track extraction helpers for simulation result CSVs."""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

from scripts.lib.common.csv import numeric_series, series_from_candidates


def extract_track_points(
    rows: List[Dict[str, str]],
) -> List[Tuple[float, float, float]]:
    xs = series_from_candidates(
        rows,
        [
            "environment.location.x_km",
            "Environment.location.x_km",
            "mission_computer.locationXYZ.x_km",
            "MissionComputer.locationXYZ.x_km",
        ],
    )
    ys = series_from_candidates(
        rows,
        [
            "environment.location.y_km",
            "Environment.location.y_km",
            "mission_computer.locationXYZ.y_km",
            "MissionComputer.locationXYZ.y_km",
        ],
    )
    zs = series_from_candidates(
        rows,
        [
            "environment.location.z_km",
            "Environment.location.z_km",
            "mission_computer.locationXYZ.z_km",
            "MissionComputer.locationXYZ.z_km",
        ],
    )

    lats = series_from_candidates(
        rows,
        [
            "mission_computer.locationLLA.latitude_deg",
            "MissionComputer.locationLLA.latitude_deg",
        ],
    )
    if (not xs or not ys) and lats:
        lons = series_from_candidates(
            rows,
            [
                "mission_computer.locationLLA.longitude_deg",
                "MissionComputer.locationLLA.longitude_deg",
            ],
        )
        alts_m = series_from_candidates(
            rows,
            [
                "mission_computer.locationLLA.altitude_m",
                "MissionComputer.locationLLA.altitude_m",
            ],
        )
        if lats and lons:
            lat0 = lats[0]
            lon0 = lons[0]
            lat0_rad = math.radians(lat0)
            xs = [111.0 * (lat - lat0) for lat in lats]
            ys = [111.0 * math.cos(lat0_rad) * (lon - lon0) for lon in lons]
            zs = [alt / 1000.0 for alt in alts_m] if alts_m else [0.0 for _ in lats]

    n = min(len(xs), len(ys), len(zs))
    return [(xs[i], ys[i], zs[i]) for i in range(n)]
