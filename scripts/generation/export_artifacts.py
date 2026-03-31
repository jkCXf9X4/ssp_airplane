#!/usr/bin/env python3
"""Export all generated artifacts derived directly from the SysML architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from pycps_sysmlv2 import SysMLParser, json_dumps

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pyssp_sysml2.fmi import generate_model_descriptions
from pyssp_sysml2.ssd import generate_ssd
from pyssp_sysml2.ssv import generate_parameter_set

from scripts.common.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, GENERATED_DIR, COMMON_MODEL_DIR, ensure_parent_dir
from scripts.generation.generate_c_interface_defs import generate_headers
from scripts.generation.generate_interface_defs import generate_modelica_package
from scripts.generation.normalize_generated_metadata import (
    normalize_model_description_timestamps,
    normalize_ssd_xml,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", type=Path, default=ARCHITECTURE_DIR)
    parser.add_argument("--generated-dir", type=Path, default=GENERATED_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    generated_dir = args.generated_dir
    architecture = SysMLParser(args.architecture).parse()

    arch_snapshot = generated_dir / "arch_def.json"
    ensure_parent_dir(arch_snapshot)
    arch_snapshot.write_text(json_dumps(architecture, []))

    interface_output = COMMON_MODEL_DIR / "modelica" / "AircraftCommon" / "GeneratedInterfaces.mo"
    ensure_parent_dir(interface_output)
    interface_output.write_text(generate_modelica_package(architecture.port_definitions), encoding="utf-8")

    generate_headers(args.architecture, generated_dir / "interfaces")
    model_descriptions = generate_model_descriptions(
        args.architecture,
        generated_dir / "model_descriptions",
        COMPOSITION_NAME,
    )
    normalize_model_description_timestamps(model_descriptions)
    generate_parameter_set(args.architecture, generated_dir / "parameters.ssv", COMPOSITION_NAME)
    ssd_path = generate_ssd(args.architecture, generated_dir / "SystemStructure.ssd", COMPOSITION_NAME)
    normalize_ssd_xml(ssd_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
