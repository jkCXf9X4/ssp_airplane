"""Export the full set of generated artifacts from the SysML architecture.

Orchestrator over the pyssp ecosystem generators:

- ``pycps_sysml2.load`` parses the architecture once;
- ``pyfmi_sml2`` emits the C/C++ interface headers and the per-component FMI
  model descriptions;
- ``pyssp_sml2`` emits the SystemStructure.ssd and the scenario/analysis
  artifacts (analysis.json + MissionScenario.ssv + HighAltitudeIntercept.ssm).

The Modelica interface package is emitted here (rebased on ``pycps_sml2``) so
the airplane models keep their pinned ``AircraftCommon.GeneratedInterfaces``
layout; we deliberately do not adopt ``pyfmi_sml2.modelica`` because its
package layout differs from the one the models import.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from pycps_sysml2 import load
from pyfmi_sysml2.c_interface import generate_c_headers
from pyfmi_sysml2.model_description import generate_model_description
from pyssp_sysml2.artifacts.analysis import generate_analysis
from pyssp_sysml2.artifacts.ssd import generate_ssd

from scripts.lib.artifacts.sysml_export.modelica_headers import generate_modelica_package
from scripts.lib.paths import (
    ANALYSIS_COMPOSITION,
    ARCHITECTURE_DIR,
    GENERATED_DIR,
    GENERATED_MODELICA_INTERFACE_FILE,
    MODEL_COMPOSITION,
    ensure_parent_dir,
)

# Fixed, timezone-aware generation stamp so modelDescription.xml output is
# reproducible.
FIXED_GENERATION_TIME = datetime(2000, 1, 1, tzinfo=timezone.utc)

_PACKAGE_MO = (
    "within ;\n"
    "package AircraftCommon\n"
    '  annotation(uses(Modelica(version="4.0.0")));\n'
    "end AircraftCommon;\n"
)
_PACKAGE_ORDER = "Interfaces\nGeneratedInterfaces\n"
_INTERFACES_MO = (
    "within AircraftCommon;\n"
    "package Interfaces\n"
    "  connector RealInput = input Real;\n"
    "  connector RealOutput = output Real;\n"
    "end Interfaces;\n"
)


def _write_modelica_package(generated_dir: Path) -> None:
    common_dir = generated_dir / GENERATED_MODELICA_INTERFACE_FILE.parent.relative_to(GENERATED_DIR)
    ensure_parent_dir(common_dir / "package.mo")
    (common_dir / "package.mo").write_text(_PACKAGE_MO, encoding="utf-8")
    (common_dir / "package.order").write_text(_PACKAGE_ORDER, encoding="utf-8")
    (common_dir / "Interfaces.mo").write_text(_INTERFACES_MO, encoding="utf-8")


def export_artifacts(
    architecture_path: Path = ARCHITECTURE_DIR,
    generated_dir: Path = GENERATED_DIR,
) -> None:
    architecture = load(architecture_path)

    _write_modelica_package(generated_dir)
    interface_output = generated_dir / GENERATED_MODELICA_INTERFACE_FILE.parent.relative_to(GENERATED_DIR) / GENERATED_MODELICA_INTERFACE_FILE.name
    ensure_parent_dir(interface_output)
    interface_output.write_text(generate_modelica_package(architecture), encoding="utf-8")

    generate_c_headers(
        architecture,
        generated_dir / "interfaces",
        composition=MODEL_COMPOSITION,
        base_index=1,
    )

    generate_model_description(
        architecture,
        generated_dir / "model_descriptions",
        composition=MODEL_COMPOSITION,
        generation_time=FIXED_GENERATION_TIME,
        base_index=1,
    )

    generate_ssd(
        architecture_path,
        generated_dir / "SystemStructure.ssd",
        MODEL_COMPOSITION,
        base_index=1,
    )

    generate_analysis(
        architecture_path,
        generated_dir / "analysis",
        ANALYSIS_COMPOSITION,
        model_name="aircraft",
        base_index=1,
    )