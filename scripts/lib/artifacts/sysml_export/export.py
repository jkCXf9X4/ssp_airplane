"""Export the generated artifacts for the branch's default composition.

Orchestrator over the pyssp ecosystem generators:

- ``pycps_sysml2.load`` parses the architecture once;
- ``pyfmi_sysml2`` emits the Modelica interface package;
- ``pyssp_sysml2`` emits the SystemStructure.ssd and the scenario/analysis
  artifacts (analysis.json + NominalMission.ssv + WorkshopMission.ssm).

The bridge is not part of the workshop composition, so no native runtime or
bridge model description is generated here.
"""
from __future__ import annotations

from pathlib import Path

from pycps_sysml2 import load
from pyfmi_sysml2 import generate_modelica
from pyssp_sysml2.artifacts.analysis import generate_analysis
from pyssp_sysml2.artifacts.ssd import generate_ssd

from scripts.lib.paths import (
    ANALYSIS_COMPOSITION,
    ARCHITECTURE_FILE,
    GENERATED_DIR,
    MODEL_COMPOSITION,
)


def export_artifacts(
    architecture_path: Path = ARCHITECTURE_FILE,
    generated_dir: Path = GENERATED_DIR,
) -> None:
    architecture = load(architecture_path)

    generate_modelica(
        architecture,
        generated_dir / "modelica",
        package="AircraftCommon",
        composition=MODEL_COMPOSITION,
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
