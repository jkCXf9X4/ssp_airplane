"""Export the full set of generated artifacts from the SysML architecture.

Orchestrator over the pyssp ecosystem generators:

- ``pycps_sysml2.load`` parses the architecture once;
- ``pyfmi_sysml`` emits the Modelica interface package;
- ``pyssp_sysml2`` emits the SystemStructure.ssd and the scenario/analysis
  artifacts (analysis.json + MissionScenario.ssv + HighAltitudeIntercept.ssm).

Every component is a Modelica FMU or an externally built FMU, so no native C
interface, runtime, or model description is generated here.
"""
from __future__ import annotations

from pathlib import Path

from pycps_sysml2 import core_definitions, load
from pyfmi_rpr import rpr_entity
from pyssp_sysml2.artifacts.analysis import generate_analysis
from pyssp_sysml2.artifacts.ssd import generate_ssd

from scripts.lib.paths import (
    ANALYSIS_COMPOSITION,
    ARCHITECTURE_DIR,
    GENERATED_DIR,
    MODEL_COMPOSITION,
)

try:  # current release name; the older pinned install exposes pyfmi_sysml2
    from pyfmi_sysml import generate_modelica
except ImportError:  # pragma: no cover - depends on the installed distribution
    from pyfmi_sysml2 import generate_modelica


def export_artifacts(
    architecture_path: Path = ARCHITECTURE_DIR,
    generated_dir: Path = GENERATED_DIR,
) -> None:
    architecture = load(architecture_path, core_definitions(), rpr_entity())

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
        includes=[core_definitions(), rpr_entity()],
        base_index=1,
    )

    generate_analysis(
        architecture_path,
        generated_dir / "analysis",
        ANALYSIS_COMPOSITION,
        model_name="aircraft",
        includes=[core_definitions(), rpr_entity()],
        base_index=1,
    )
