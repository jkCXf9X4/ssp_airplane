"""Check that Modelica interface variables match SysML port definitions."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

from pycps_sysmlv2 import NodeType, SysMLParser

from scripts.lib.common.modelica import MODELICA_MODEL_SPECS
from scripts.lib.paths import ARCHITECTURE_DIR, COMPOSITION_NAME

DEFAULT_ARCH_DIR = ARCHITECTURE_DIR

INTERFACE_DECL_RE = re.compile(
    r"\b(?P<direction>input|output)\s+GI\.(?P<record>\w+)\s+(?P<var>\w+)",
    re.MULTILINE,
)


def _collect_architecture_data(
    architecture,
) -> Tuple[Dict[str, Set[str]], Dict[str, Dict[str, Tuple[str, str]]]]:
    members: Dict[str, Set[str]] = {}
    part_ports: Dict[str, Dict[str, Tuple[str, str]]] = {}

    for name, definition in architecture.port_definitions.items():
        members[name] = set(definition.defs(NodeType.Attribute).keys())

    for part_name, part in architecture.part_definitions.items():
        if part_name == COMPOSITION_NAME:
            continue
        part_ports[part_name] = {
            port.name: (port.direction, port.type)
            for port in part.refs(NodeType.Port).values()
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
def verify_modelica_variables(architecture_path: Path = DEFAULT_ARCH_DIR) -> int:
    architecture = SysMLParser(architecture_path).parse()
    members, part_ports = _collect_architecture_data(architecture)

    overall_issues: List[str] = []
    for mo_file in (spec.model_file for spec in MODELICA_MODEL_SPECS):
        if not mo_file.exists():
            print(f"Model file not found: {mo_file}", file=sys.stderr)
            return 1
        overall_issues.extend(_scan_file(mo_file, members, part_ports))

    if overall_issues:
        print("Variable naming verification failed:")
        for issue in overall_issues:
            print(f" - {issue}")
        return 2

    print("All Modelica interface variable usages match the architecture.")
    return 0
