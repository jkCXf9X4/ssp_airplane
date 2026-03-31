"""Generate plots from simulation result artifacts."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Dict, List, Optional

from scripts.lib.common.geo import project_waypoints_to_local_km
from scripts.lib.common.csv import numeric_series, read_result_rows, series_from_candidates
from scripts.lib.results.track import extract_track_points


def plot_flight_path(
    result_file: Path, scenario_points: List[Dict[str, float]], output_path: Path
) -> Optional[Path]:
    if os.environ.get("SIM_SKIP_PLOTS") == "1":
        return None
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None

    rows = read_result_rows(result_file)
    xs = series_from_candidates(
        rows,
        [
            "environment.location.x_km",
            "Environment.location.x_km",
        ],
    )
    ys = series_from_candidates(
        rows,
        [
            "environment.location.y_km",
            "Environment.location.y_km",
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
        if lats and lons:
            lat0 = lats[0]
            lon0 = lons[0]
            lat0_rad = math.radians(lat0)
            xs = [111.0 * (lat - lat0) for lat in lats]
            ys = [111.0 * math.cos(lat0_rad) * (lon - lon0) for lon in lons]

    if not xs or not ys:
        return None

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(xs, ys, label="Flight path", color="#1f77b4")

    if scenario_points:
        wp_x = [p["x_km"] for p in scenario_points]
        wp_y = [p["y_km"] for p in scenario_points]
        ax.plot(wp_x, wp_y, "o--", label="Waypoints", color="#d62728")

    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_title("Flight path vs waypoints (local frame)")
    ax.legend()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_flight_path_3d(
    result_file: Path, scenario_points: List[Dict[str, float]], output_path: Path
) -> Optional[Path]:
    if os.environ.get("SIM_SKIP_PLOTS") == "1":
        return None
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    except Exception:
        return None

    rows = read_result_rows(result_file)
    track_points = extract_track_points(rows)
    if not track_points:
        return None

    xs, ys, zs = zip(*track_points)
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(xs, ys, zs, label="Flight path", color="#1f77b4")

    if scenario_points:
        wp_x = [p["x_km"] for p in scenario_points]
        wp_y = [p["y_km"] for p in scenario_points]
        wp_z = [p.get("z_km", 0.0) for p in scenario_points]
        ax.plot(wp_x, wp_y, wp_z, "o--", label="Waypoints", color="#d62728")

    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_zlabel("Z [km]")
    ax.set_title("Flight path vs waypoints (3D local frame)")
    ax.legend()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_fuel_altitude_time(result_file: Path, output_path: Path) -> Optional[Path]:
    if os.environ.get("SIM_SKIP_PLOTS") == "1":
        return None
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None

    rows = read_result_rows(result_file)
    time_series = numeric_series(rows, "time")
    altitude_km = series_from_candidates(
        rows,
        [
            "environment.location.z_km",
            "Environment.location.z_km",
            "mission_computer.locationXYZ.z_km",
            "MissionComputer.locationXYZ.z_km",
        ],
    )
    if not altitude_km:
        altitude_m = series_from_candidates(
            rows,
            [
                "mission_computer.locationLLA.altitude_m",
                "MissionComputer.locationLLA.altitude_m",
            ],
        )
        altitude_km = [alt / 1000.0 for alt in altitude_m]
    fuel_remaining = series_from_candidates(
        rows,
        [
            "fuel_system.fuelState.fuel_remaining_kg",
            "FuelSystem.fuelState.fuel_remaining_kg",
        ],
    )

    fig, ax_alt = plt.subplots(figsize=(7, 5))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if altitude_km:
        alt_len = min(len(time_series), len(altitude_km))
        ax_alt.plot(
            time_series[:alt_len],
            altitude_km[:alt_len],
            color="#1f77b4",
            label="Altitude (km)",
        )
        ax_alt.set_ylabel("Altitude [km]", color="#1f77b4")
        ax_alt.tick_params(axis="y", labelcolor="#1f77b4")

    ax_alt.set_xlabel("Time [s]")

    fuel_axis = None
    if fuel_remaining:
        fuel_axis = ax_alt.twinx()
        fuel_len = min(len(time_series), len(fuel_remaining))
        fuel_axis.plot(
            time_series[:fuel_len],
            fuel_remaining[:fuel_len],
            color="#d62728",
            label="Fuel remaining (kg)",
        )
        fuel_axis.set_ylabel("Fuel remaining [kg]", color="#d62728")
        fuel_axis.tick_params(axis="y", labelcolor="#d62728")
    lines, labels = ax_alt.get_legend_handles_labels()
    if fuel_axis:
        fuel_lines, fuel_labels = fuel_axis.get_legend_handles_labels()
        lines += fuel_lines
        labels += fuel_labels
    if lines:
        ax_alt.legend(lines, labels, loc="best")

    ax_alt.set_title("Altitude and fuel level vs time")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def _load_scenario_points(scenario_path: Optional[Path]) -> List[Dict[str, float]]:
    if not scenario_path:
        return []
    scenario = json.loads(scenario_path.read_text())
    points = scenario.get("points") or []
    return project_waypoints_to_local_km(points) if points else []


def generate_plots(
    results_csv: Path,
    scenario: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    plot_path: bool = False,
    plot_3d: bool = False,
    plot_fuel_altitude: bool = False,
) -> Dict[str, Optional[str]]:
    output_dir = output_dir or results_csv.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    scenario_points = _load_scenario_points(scenario)
    stem = results_csv.stem.replace("_results", "")

    generated: Dict[str, Optional[str]] = {}
    if plot_path:
        path_out = output_dir / f"{stem}_path.png"
        plotted = plot_flight_path(results_csv, scenario_points, path_out)
        if plotted:
            generated["plot_path"] = str(plotted)
    if plot_3d:
        path3d_out = output_dir / f"{stem}_path3d.png"
        plotted3d = plot_flight_path_3d(results_csv, scenario_points, path3d_out)
        if plotted3d:
            generated["plot3d_path"] = str(plotted3d)
    if plot_fuel_altitude:
        fuel_alt_out = output_dir / f"{stem}_fuel_altitude.png"
        plotted_fuel = plot_fuel_altitude_time(results_csv, fuel_alt_out)
        if plotted_fuel:
            generated["plot_fuel_altitude_path"] = str(plotted_fuel)
    return generated
