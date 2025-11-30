from __future__ import annotations

import argparse
import csv
import json
import math
import os
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from scripts.utils.map_geometry import project_waypoints_to_local_km


def _numeric_series(
    rows: Sequence[Dict[str, str]], key: str, cast=float
) -> List[float]:
    values: List[float] = []
    for row in rows:
        raw = row.get(key, "")
        if raw is None:
            continue
        raw_str = str(raw).strip()
        if not raw_str:
            continue
        try:
            values.append(cast(raw_str))
        except ValueError:
            try:
                values.append(cast(raw_str.replace(",", "")))
            except ValueError:
                continue
    return values


def _series_from_candidates(
    rows: Sequence[Dict[str, str]], keys: Sequence[str], cast=float
) -> List[float]:
    for key in keys:
        series = _numeric_series(rows, key, cast=cast)
        if series:
            return series
    return []


def _read_result_rows(result_file: Path) -> List[Dict[str, str]]:
    with result_file.open() as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def extract_track_points(
    rows: List[Dict[str, str]],
) -> List[Tuple[float, float, float]]:
    xs = _numeric_series(rows, "Environment.location.x_km") or _numeric_series(
        rows, "MissionComputer.locationXYZ.x_km"
    )
    ys = _numeric_series(rows, "Environment.location.y_km") or _numeric_series(
        rows, "MissionComputer.locationXYZ.y_km"
    )
    zs = _numeric_series(rows, "Environment.location.z_km") or _numeric_series(
        rows, "MissionComputer.locationXYZ.z_km"
    )

    # Backward-compatibility for legacy lat/lon recordings in existing CSVs
    if (not xs or not ys) and _numeric_series(
        rows, "MissionComputer.locationLLA.latitude_deg"
    ):
        lats = _numeric_series(rows, "MissionComputer.locationLLA.latitude_deg")
        lons = _numeric_series(rows, "MissionComputer.locationLLA.longitude_deg")
        alts_m = _numeric_series(rows, "MissionComputer.locationLLA.altitude_m")
        if lats and lons:
            lat0 = lats[0]
            lon0 = lons[0]
            lat0_rad = math.radians(lat0)
            xs = [111.0 * (lat - lat0) for lat in lats]
            ys = [111.0 * math.cos(lat0_rad) * (lon - lon0) for lon in lons]
            zs = [alt / 1000.0 for alt in alts_m] if alts_m else [0.0 for _ in lats]

    n = min(len(xs), len(ys), len(zs))
    return [(xs[i], ys[i], zs[i]) for i in range(n)]


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

    rows = _read_result_rows(result_file)
    xs = _numeric_series(rows, "Environment.location.x_km")
    ys = _numeric_series(rows, "Environment.location.y_km")

    if (not xs or not ys) and _numeric_series(
        rows, "MissionComputer.locationLLA.latitude_deg"
    ):
        lats = _numeric_series(rows, "MissionComputer.locationLLA.latitude_deg")
        lons = _numeric_series(rows, "MissionComputer.locationLLA.longitude_deg")
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

    rows = _read_result_rows(result_file)
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

    rows = _read_result_rows(result_file)
    time_series = _numeric_series(rows, "time")
    altitude_km = _numeric_series(rows, "Environment.location.z_km") or _numeric_series(
        rows, "MissionComputer.locationXYZ.z_km"
    )
    if not altitude_km and _numeric_series(
        rows, "MissionComputer.locationLLA.altitude_m"
    ):
        altitude_m = _numeric_series(rows, "MissionComputer.locationLLA.altitude_m")
        altitude_km = [alt / 1000.0 for alt in altitude_m]
    fuel_remaining = _numeric_series(
        rows, "FuelSystem.fuelState.fuel_remaining_kg"
    )

    print(fuel_remaining)


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
    fuel_level_axis = None


    lines, labels = ax_alt.get_legend_handles_labels()
    if fuel_axis:
        fuel_lines, fuel_labels = fuel_axis.get_legend_handles_labels()
        lines += fuel_lines
        labels += fuel_labels
    if fuel_level_axis:
        level_lines, level_labels = fuel_level_axis.get_legend_handles_labels()
        lines += level_lines
        labels += level_labels
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate plots from a simulation results CSV."
    )
    parser.add_argument(
        "--results-csv",
        type=Path,
        required=True,
        help="Path to the simulation results CSV.",
    )
    parser.add_argument(
        "--scenario",
        type=Path,
        default=None,
        help="Optional scenario JSON to overlay waypoints on the flight-path plots.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write plots (defaults to the results CSV directory).",
    )
    parser.add_argument(
        "--plot-path", action="store_true", help="Generate the 2D flight-path plot."
    )
    parser.add_argument(
        "--plot-3d", action="store_true", help="Generate the 3D flight-path plot."
    )
    parser.add_argument(
        "--plot-fuel-altitude",
        action="store_true",
        help="Generate the fuel remaining and altitude versus time plot.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir or args.results_csv.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    scenario_points = _load_scenario_points(args.scenario)
    stem = args.results_csv.stem.replace("_results", "")

    generated: Dict[str, Optional[str]] = {}
    if args.plot_path:
        path_out = output_dir / f"{stem}_path.png"
        plotted = plot_flight_path(args.results_csv, scenario_points, path_out)
        if plotted:
            generated["plot_path"] = str(plotted)
    if args.plot_3d:
        path3d_out = output_dir / f"{stem}_path3d.png"
        plotted3d = plot_flight_path_3d(args.results_csv, scenario_points, path3d_out)
        if plotted3d:
            generated["plot3d_path"] = str(plotted3d)
    if args.plot_fuel_altitude:
        fuel_alt_out = output_dir / f"{stem}_fuel_altitude.png"
        plotted_fuel = plot_fuel_altitude_time(args.results_csv, fuel_alt_out)
        if plotted_fuel:
            generated["plot_fuel_altitude_path"] = str(plotted_fuel)

    print(json.dumps(generated, indent=2))


if __name__ == "__main__":
    main()
