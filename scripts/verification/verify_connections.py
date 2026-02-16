#!/usr/bin/env python3
"""Verify SysML connector endpoints for consistency."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR
from pycps_sysmlv2 import SysMLArchitecture, SysMLPortReference, load_architecture
from scripts.utils.sysml_compat import (
    architecture_connections,
    composition_components,
    part_ports,
)

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR


def _build_port_index(architecture: SysMLArchitecture) -> Dict[Tuple[str, str], SysMLPortReference]:
    index: Dict[Tuple[str, str], SysMLPortReference] = {}
    for comp_name, part in composition_components(architecture):
        for port in part_ports(part):
            index[(comp_name, port.name)] = port
    return index


def verify_connections(architecture_path: Path) -> int:
    architecture = load_architecture(architecture_path)
    components = {name for name, _ in composition_components(architecture)}
    port_index = _build_port_index(architecture)
    issues: List[str] = []

    for connector in architecture_connections(architecture):
        start_comp = connector.src_component
        end_comp = connector.dst_component
        start_port = connector.src_port
        end_port = connector.dst_port

        if start_comp not in components:
            issues.append(f"Unknown component in 'from': {start_comp}.{start_port}")
            continue
        if end_comp not in components:
            issues.append(f"Unknown component in 'to': {end_comp}.{end_port}")
            continue

        start_def = port_index.get((start_comp, start_port))
        end_def = port_index.get((end_comp, end_port))
        if not start_def:
            issues.append(f"Port {start_port} missing on component {start_comp}")
            continue
        if not end_def:
            issues.append(f"Port {end_port} missing on component {end_comp}")
            continue

        if start_def.direction == "in" and end_def.direction == "in":
            issues.append(f"In-to-in connection detected: {start_comp}.{start_port} -> {end_comp}.{end_port}")
        if start_def.direction == "out" and end_def.direction == "out":
            issues.append(f"Out-to-out connection detected: {start_comp}.{start_port} -> {end_comp}.{end_port}")

    if issues:
        print("Connector verification failed:")
        for issue in issues:
            print(f" - {issue}")
        return 2

    print("All connectors resolved to valid component ports.")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Directory containing the SysML .sysml sections.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return verify_connections(args.architecture)


if __name__ == "__main__":
    raise SystemExit(main())
