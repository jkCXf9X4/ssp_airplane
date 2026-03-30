#!/usr/bin/env python3
"""Generate FMI 2.0 `modelDescription.xml` stubs for every component in the SysML architecture."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pyssp_sysml2.fmi import generate_model_descriptions as generate_upstream_model_descriptions

from scripts.common.paths import ARCHITECTURE_DIR, COMPOSITION_NAME, GENERATED_DIR

DEFAULT_ARCH_PATH = ARCHITECTURE_DIR
DEFAULT_OUTPUT_DIR = GENERATED_DIR / "model_descriptions"
FIXED_GENERATION_TIMESTAMP = "2000-00-00T00:00:00Z"


def _normalize_generation_timestamp(paths: list[Path]) -> list[Path]:
    for path in paths:
        tree = ET.parse(path)
        root = tree.getroot()
        root.set("generationDateAndTime", FIXED_GENERATION_TIMESTAMP)
        ET.indent(tree, space="  ", level=0)
        tree.write(path, encoding="utf-8", xml_declaration=True)
    return paths


def generate_model_descriptions(
    architecture: Path,
    output_dir: Path,
    composition: str,
) -> list[Path]:
    written = generate_upstream_model_descriptions(
        architecture,
        output_dir,
        composition,
    )
    return _normalize_generation_timestamp(written)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCH_PATH,
        help="Path to the SysML architecture directory or a file within it.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory that will contain one sub-folder per component, each with a modelDescription.xml.",
    )
    parser.add_argument(
        "--composition",
        default=COMPOSITION_NAME,
        help="Composition part definition to export.",
    )
    args = parser.parse_args(argv)

    try:
        written = generate_model_descriptions(
            args.architecture,
            args.output_dir,
            args.composition,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    for path in written:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
