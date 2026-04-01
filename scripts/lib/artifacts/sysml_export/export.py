"""Export the full set of generated artifacts from the SysML architecture."""
from __future__ import annotations

from pathlib import Path
from pycps_sysmlv2 import SysMLParser, json_dumps

from pyssp_sysml2.fmi import generate_model_descriptions
from pyssp_sysml2.ssd import generate_ssd
from pyssp_sysml2.ssv import generate_parameter_set

from scripts.lib.paths import (
    ARCHITECTURE_DIR,
    COMPOSITION_NAME,
    GENERATED_DIR,
    GENERATED_MODELICA_INTERFACE_FILE,
    ensure_parent_dir,
)
from scripts.lib.artifacts.sysml_export.c_headers import generate_headers
from scripts.lib.artifacts.sysml_export.modelica_headers import generate_modelica_package
from scripts.lib.common.xml import (
    normalize_model_description_timestamps,
    normalize_ssd_xml,
)


def export_artifacts(
    architecture_path: Path = ARCHITECTURE_DIR,
    generated_dir: Path = GENERATED_DIR,
) -> None:
    architecture = SysMLParser(architecture_path).parse()

    arch_snapshot = generated_dir / "arch_def.json"
    ensure_parent_dir(arch_snapshot)
    arch_snapshot.write_text(json_dumps(architecture, []))

    common_modelica_dir = generated_dir / GENERATED_MODELICA_INTERFACE_FILE.parent.relative_to(GENERATED_DIR)
    ensure_parent_dir(common_modelica_dir / "package.mo")
    (common_modelica_dir / "package.mo").write_text(
        "within ;\npackage AircraftCommon\n  annotation(uses(Modelica(version=\"4.0.0\")));\nend AircraftCommon;\n",
        encoding="utf-8",
    )
    (common_modelica_dir / "package.order").write_text(
        "Interfaces\nGeneratedInterfaces\n",
        encoding="utf-8",
    )
    (common_modelica_dir / "Interfaces.mo").write_text(
        "within AircraftCommon;\npackage Interfaces\n  connector RealInput = input Real;\n  connector RealOutput = output Real;\nend Interfaces;\n",
        encoding="utf-8",
    )

    interface_output = common_modelica_dir / GENERATED_MODELICA_INTERFACE_FILE.name
    ensure_parent_dir(interface_output)
    interface_output.write_text(generate_modelica_package(architecture.port_definitions), encoding="utf-8")

    generate_headers(architecture_path, generated_dir / "interfaces")
    model_descriptions = generate_model_descriptions(
        architecture_path,
        generated_dir / "model_descriptions",
        COMPOSITION_NAME,
    )
    normalize_model_description_timestamps(model_descriptions)
    generate_parameter_set(architecture_path, generated_dir / "parameters.ssv", COMPOSITION_NAME)
    ssd_path = generate_ssd(architecture_path, generated_dir / "SystemStructure.ssd", COMPOSITION_NAME)
    normalize_ssd_xml(ssd_path)
