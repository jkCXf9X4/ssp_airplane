"""Check that Modelica models consume the generated interface source of truth."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List

from pycps_sysml2 import core_definitions, load
from pyfmi_rpr import rpr_entity

from scripts.lib.common.modelica import MODELICA_MODEL_SPECS
from scripts.lib.paths import ARCHITECTURE_DIR

DEFAULT_ARCH_DIR = ARCHITECTURE_DIR

CONNECTOR_DECL_RE = re.compile(r"^\s*(?P<direction>input|output)\b", re.MULTILINE)


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _scan_file(path: Path, class_name: str) -> List[str]:
    text = path.read_text()
    issues: List[str] = []
    extends_re = re.compile(
        rf"\bextends\s+AircraftCommon\.{re.escape(class_name)}_Interface\s*;"
    )
    match = extends_re.search(text)
    if match is None:
        model_re = re.compile(rf"\bmodel\s+{re.escape(class_name)}\b")
        model_match = model_re.search(text)
        line = _line_of(text, model_match.start()) if model_match else 1
        issues.append(
            f"{path}:{line}: model does not extend AircraftCommon.{class_name}_Interface."
        )
    for connector in CONNECTOR_DECL_RE.finditer(text):
        line = _line_of(text, connector.start())
        issues.append(
            f"{path}:{line}: model declares its own {connector.group('direction')} connector."
        )
    return issues


def verify_modelica_variables(architecture_path: Path = DEFAULT_ARCH_DIR) -> int:
    architecture = load(architecture_path, core_definitions(), rpr_entity())
    part_names = set(architecture.part_definitions)

    overall_issues: List[str] = []
    for spec in MODELICA_MODEL_SPECS:
        mo_file = spec.model_file
        if not mo_file.exists():
            print(f"Model file not found: {mo_file}", file=sys.stderr)
            return 1
        if spec.class_name not in part_names:
            overall_issues.append(
                f"{mo_file}: part '{spec.class_name}' is not defined in the architecture."
            )
        overall_issues.extend(_scan_file(mo_file, spec.class_name))

    if overall_issues:
        print("Modelica interface verification failed:")
        for issue in overall_issues:
            print(f" - {issue}")
        return 2

    print("All Modelica models extend their generated AircraftCommon interface.")
    return 0
