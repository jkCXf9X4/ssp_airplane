#!/usr/bin/env python3
"""Generate randomized flight scenarios built from GeodeticLLA waypoints."""
from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List

from scripts.utils.map_geometry import destination_point, haversine_distance_km


@dataclass
class GeodeticLLA:
    latitude_deg: float
    longitude_deg: float
    altitude_m: float


def random_segments(count: int, total: float) -> List[float]:
    """Randomly split total distance into 'count' positive segments."""
    weights = [random.random() + 0.1 for _ in range(count)]
    weight_sum = sum(weights)
    return [total * w / weight_sum for w in weights]


def generate_scenario(
    num_points: int,
    min_distance_km: float,
    max_distance_km: float,
    min_altitude_m: float,
    max_altitude_m: float,
) -> dict:
    total_distance = random.uniform(min_distance_km, max_distance_km)
    segment_distances = random_segments(num_points - 1, total_distance)

    start = GeodeticLLA(
        latitude_deg=random.uniform(-45.0, 45.0),
        longitude_deg=random.uniform(-120.0, 120.0),
        altitude_m=0.0,
    )
    points: List[GeodeticLLA] = [start]

    current = start
    for idx, distance_km in enumerate(segment_distances, start=1):
        bearing = random.uniform(0.0, 2 * math.pi)
        dest = destination_point(
            current.latitude_deg, current.longitude_deg, distance_km, bearing
        )
        next_point = GeodeticLLA(dest["latitude_deg"], dest["longitude_deg"], 0.0)
        if idx == len(segment_distances):
            next_point.altitude_m = 0.0
        else:
            next_point.altitude_m = random.uniform(min_altitude_m, max_altitude_m)
        points.append(next_point)
        current = next_point

    total_distance_calc = haversine_distance_km(
        [
            {
                "latitude_deg": p.latitude_deg,
                "longitude_deg": p.longitude_deg,
            }
            for p in points
        ]
    )
    return {
        "points": [
            {
                "latitude_deg": round(p.latitude_deg, 6),
                "longitude_deg": round(p.longitude_deg, 6),
                "altitude_m": round(p.altitude_m, 2),
            }
            for p in points
        ],
        "total_distance_km": round(total_distance_calc, 2),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Destination JSON file.")
    parser.add_argument("--points", type=int, default=None, help="Number of scenario points (3-10).")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed.")
    parser.add_argument("--min-distance", type=float, default=100.0)
    parser.add_argument("--max-distance", type=float, default=1000.0)
    parser.add_argument("--min-altitude", type=float, default=100.0)
    parser.add_argument("--max-altitude", type=float, default=10000.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    if args.points is not None and not (3 <= args.points <= 10):
        raise SystemExit("--points must be between 3 and 10")
    num_points = args.points or random.randint(3, 10)
    scenario = generate_scenario(
        num_points=num_points,
        min_distance_km=args.min_distance,
        max_distance_km=args.max_distance,
        min_altitude_m=args.min_altitude,
        max_altitude_m=args.max_altitude,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scenario, indent=2))
    print(f"Wrote scenario with {len(scenario['points'])} points to {args.output}")


if __name__ == "__main__":
    main()
