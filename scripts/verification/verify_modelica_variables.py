#!/usr/bin/env python3
"""Verify Modelica interface names/fields match SysML port definitions."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.common.paths import ARCHITECTURE_DIR, MODELS_DIR
from scripts.utils.sysml_helpers import load_architecture

DEFAULT_ARCH_DIR = ARCHITECTURE_DIR
DEFAULT_MODELS_DIR = MODELS_DIR / "Aircraft"

INTERFACE_DECL_RE = re.compile(
    r"\b(?P<direction>input|output)\s+GI\.(?P<record>\w+)\s+(?P<var>\w+)",
    re.MULTILINE,
)


def _collect_architecture_data(
    architecture: SysMLArchitecture,
) -> Tuple[Dict[str, Set[str]], Dict[str, Dict[str, Tuple[str, str]]]]:
    members: Dict[str, Set[str]] = {}
    part_ports: Dict[str, Dict[str, Tuple[str, str]]] = {}

    for name, definition in architecture.port_definitions.items():
        members[name] = set(definition.attributes.keys())

    for part_name, part in architecture.parts.items():
        part_ports[part_name] = {
            port.name: (port.direction, port.payload) for port in part.ports
        }

    return members, part_ports


def _scan_file(
    path: Path,
    members: Dict[str, Set[str]],
    part_ports: Dict[str, Dict[str, Tuple[str, str]]],
) -> List[str]:
    text = path.read_text()
    issues: List[str] = []
    declarations = list(INTERFACE_DECL_RE.finditer(text))
    if not declarations:
        return issues
    part_name = path.stem
    ports = part_ports.get(part_name)
    for match in declarations:
        direction = match.group("direction")
        record = match.group("record")
        var = match.group("var")
        if record not in members:
            issues.append(f"{path}: Interface {record} referenced by {var} "
                          "is not present in architecture definitions.")
            continue
        used = set(re.findall(rf"\b{re.escape(var)}\.(\w+)", text))
        missing = sorted(field for field in used if field not in members[record])
        if missing:
            formatted = ", ".join(missing)
            issues.append(
                f"{path}: {record} field(s) {formatted} not defined in architecture."
            )
        if ports is None:
            continue
        if var not in ports:
            issues.append(
                f"{path}: Interface variable '{var}' ({record}) not defined on SysML part '{part_name}'."
            )
            continue
        expected_dir, expected_payload = ports[var]
        dir_map = {"input": "in", "output": "out"}
        if dir_map.get(direction) != expected_dir:
            issues.append(
                f"{path}: Port '{var}' direction mismatch (Modelica {direction}, SysML {expected_dir})."
            )
        if record != expected_payload:
            issues.append(
                f"{path}: Port '{var}' type mismatch (Modelica {record}, SysML {expected_payload})."
            )
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_DIR,
        help="Path to the SysML architecture directory or file.",
    )
    parser.add_argument(
        "--models-dir",
        type=Path,
        default=DEFAULT_MODELS_DIR,
        help="Directory containing Modelica models to check.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    architecture = load_architecture(args.architecture)
    members, part_ports = _collect_architecture_data(architecture)

    if not args.models_dir.exists():
        print(f"Model directory not found: {args.models_dir}", file=sys.stderr)
        return 1

    overall_issues: List[str] = []
    for mo_file in sorted(args.models_dir.glob("*.mo")):
        overall_issues.extend(_scan_file(mo_file, members, part_ports))

    if overall_issues:
        print("Variable naming verification failed:")
        for issue in overall_issues:
            print(f" - {issue}")
        return 2

    print("All Modelica interface variable usages match the architecture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
