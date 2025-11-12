#!/usr/bin/env python3
"""Verify SysML connector endpoints for consistency."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

from sysml_loader import load_architecture


def build_port_index(components: List[dict]) -> Dict[Tuple[str, str], dict]:
    index: Dict[Tuple[str, str], dict] = {}
    for comp in components:
        comp_id = comp["id"]
        for port in comp.get("ports", []):
            index[(comp_id, port["name"])] = port
    return index


def verify_connections(architecture: Path) -> int:
    data = load_architecture(architecture)
    components = {comp["id"]: comp for comp in data["components"]}
    port_index = build_port_index(data["components"])
    issues: List[str] = []

    for connector in data["connectors"]:
        start = connector["from"]
        end = connector["to"]
        try:
            start_comp, start_port = start.rsplit(".", 1)
            end_comp, end_port = end.rsplit(".", 1)
        except ValueError:
            issues.append(f"Malformed connector endpoints: {start} -> {end}")
            continue

        if start_comp not in components:
            issues.append(f"Unknown component in 'from': {start}")
            continue
        if end_comp not in components:
            issues.append(f"Unknown component in 'to': {end}")
            continue

        start_def = port_index.get((start_comp, start_port))
        end_def = port_index.get((end_comp, end_port))
        if not start_def:
            issues.append(f"Port {start_port} missing on component {start_comp}")
            continue
        if not end_def:
            issues.append(f"Port {end_port} missing on component {end_comp}")
            continue

        if start_def.get("direction") == "in" and end_def.get("direction") == "in":
            issues.append(f"In-to-in connection detected: {start} -> {end}")
        if start_def.get("direction") == "out" and end_def.get("direction") == "out":
            issues.append(f"Out-to-out connection detected: {start} -> {end}")

    if issues:
        print("Connector verification failed:")
        for issue in issues:
            print(f" - {issue}")
        return 2

    print("All connectors resolved to valid component ports.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=Path("architecture/aircraft_architecture.sysml"),
        help="Path to the SysML architecture file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise SystemExit(verify_connections(args.architecture))


if __name__ == "__main__":
    main()
