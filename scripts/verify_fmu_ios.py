#!/usr/bin/env python3
"""Verify that every SysML-defined input/output exists in the exported FMUs."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import xml.etree.ElementTree as ET
import zipfile

from utils.sysmlv2_arch_parser import SysMLArchitecture, SysMLPartDefinition, parse_sysml_folder

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCH_PATH = REPO_ROOT / "architecture"
DEFAULT_FMU_DIR = REPO_ROOT / "build" / "fmus"
VALID_DIRECTIONS = {"in", "out"}


def _load_scalar_variables(fmu_path: Path) -> Dict[str, Optional[str]]:
    try:
        with zipfile.ZipFile(fmu_path) as archive:
            with archive.open("modelDescription.xml") as handle:
                tree = ET.parse(handle)
    except FileNotFoundError as exc:
        raise SystemExit(f"FMU file not found: {fmu_path}") from exc
    except KeyError as exc:
        raise SystemExit(f"{fmu_path} does not contain modelDescription.xml") from exc
    except zipfile.BadZipFile as exc:
        raise SystemExit(f"FMU file is not a valid zip archive: {fmu_path}") from exc

    variables: Dict[str, Optional[str]] = {}
    for scalar in tree.iterfind(".//ScalarVariable"):
        name = scalar.attrib.get("name")
        causality = scalar.attrib.get("causality")
        if name:
            variables[name] = causality
    return variables


def _resolve_parts(architecture: SysMLArchitecture, parts: Sequence[str] | None) -> Dict[str, SysMLPartDefinition]:
    if not parts:
        return architecture.parts
    subset: Dict[str, SysMLPartDefinition] = {}
    missing: List[str] = []
    for part_name in parts:
        if part_name not in architecture.parts:
            missing.append(part_name)
            continue
        subset[part_name] = architecture.parts[part_name]
    if missing:
        raise SystemExit(f"Unknown part(s) requested: {', '.join(sorted(missing))}")
    return subset


def verify_fmu_ios(arch_path: Path, fmu_dir: Path, parts: Sequence[str] | None = None) -> int:
    architecture = parse_sysml_folder(arch_path)
    target_parts = _resolve_parts(architecture, parts)
    issues: List[str] = []
    checked_parts = 0
    checked_ports = 0

    for part_name in sorted(target_parts):
        part = target_parts[part_name]
        expected: List[Tuple[str, str, str]] = []
        for port in part.ports:
            payload = port.payload_def
            if payload is None:
                issues.append(
                    f"{part_name}.{port.name} references unknown payload '{port.payload}'"
                )
                continue
            attr_names = list(payload.attributes.keys())
            if not attr_names:
                continue
            for attr_name in attr_names:
                expected.append((f"{port.name}.{attr_name}", port.direction, port.name))
        if not expected:
            continue
        fmu_path = fmu_dir / f"WingmanDrone_{part_name}.fmu"
        if not fmu_path.exists():
            issues.append(f"Missing FMU for part {part_name}: {fmu_path}")
            continue
        variables = _load_scalar_variables(fmu_path)
        checked_parts += 1

        for var_name, direction, port_name in expected:
            checked_ports += 1
            if direction.lower() not in VALID_DIRECTIONS:
                issues.append(f"Unknown direction '{direction}' on {part_name}.{port_name}")
                continue
            if var_name not in variables:
                issues.append(f"{part_name}: missing variable '{var_name}' in {fmu_path.name}")
                continue
            actual_causality = variables[var_name]
            if direction.lower() == "in" and actual_causality != "input":
                issues.append(
                    f"{part_name}: variable '{var_name}' causality {actual_causality!r} "
                    "is not marked as FMI input"
                )
            if direction.lower() == "out" and actual_causality != "output":
                issues.append(
                    f"{part_name}: variable '{var_name}' causality {actual_causality!r} "
                    "is not marked as FMI output"
                )

    if issues:
        print("FMU I/O verification failed:")
        for issue in issues:
            print(f" - {issue}")
        return 2

    print(f"Verified {checked_ports} port attributes across {checked_parts} FMUs.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Directory containing the SysML *.sysml files",
    )
    parser.add_argument(
        "--fmu-dir",
        type=Path,
        default=DEFAULT_FMU_DIR,
        help="Directory containing the exported FMUs",
    )
    parser.add_argument(
        "--parts",
        nargs="+",
        help="Subset of SysML parts to verify (default: all parts with ports)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise SystemExit(verify_fmu_ios(args.architecture, args.fmu_dir, args.parts))


if __name__ == "__main__":
    main()
