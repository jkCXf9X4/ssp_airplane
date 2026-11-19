"""Export the full set of generated artifacts from the SysML architecture.

Orchestrator over the pyssp ecosystem generators:

- ``pycps_sysml2.load`` parses the architecture once;
- ``pyfmi_sysml2`` emits the C interface headers, the C++ runtime with its model
  seam, the FMI model description, and the Modelica interface package;
- ``pyssp_sysml2`` emits the SystemStructure.ssd and the scenario/analysis
  artifacts (analysis.json + MissionScenario.ssv + HighAltitudeIntercept.ssm).
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from pycps_sysml2 import load
from pyfmi_sysml2 import (
    generate_c_runtime,
    generate_model_description,
    generate_modelica,
)
from pyssp_sysml2.artifacts.analysis import generate_analysis
from pyssp_sysml2.artifacts.ssd import generate_ssd

from scripts.lib.paths import (
    ANALYSIS_COMPOSITION,
    ARCHITECTURE_DIR,
    GENERATED_DIR,
    MODEL_COMPOSITION,
)

# Fixed, timezone-aware generation stamp so modelDescription.xml output is
# reproducible.
FIXED_GENERATION_TIME = datetime(2000, 1, 1, tzinfo=timezone.utc)


def export_artifacts(
    architecture_path: Path = ARCHITECTURE_DIR,
    generated_dir: Path = GENERATED_DIR,
) -> None:
    architecture = load(architecture_path)

    generate_c_runtime(
        architecture,
        generated_dir / "interfaces",
        composition=MODEL_COMPOSITION,
        component="UdpBridge",
        base_index=1,
    )

    generate_model_description(
        architecture,
        generated_dir / "model_descriptions",
        composition=MODEL_COMPOSITION,
        component="UdpBridge",
        generation_time=FIXED_GENERATION_TIME,
        base_index=1,
    )

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
