#!/usr/bin/env python3
"""Normalize generated artifact metadata for deterministic repository outputs."""
from __future__ import annotations

import re
from pathlib import Path
import xml.etree.ElementTree as ET

FIXED_GENERATION_TIMESTAMP = "2000-01-01T00:00:00"


def normalize_model_description_timestamps(paths: list[Path]) -> list[Path]:
    for path in paths:
        tree = ET.parse(path)
        root = tree.getroot()
        root.set("generationDateAndTime", FIXED_GENERATION_TIMESTAMP)
        ET.indent(tree, space="  ", level=0)
        tree.write(path, encoding="utf-8", xml_declaration=True)
    return paths


def normalize_ssd_xml(path: Path) -> Path:
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'generationDateAndTime="[^"]+"',
        f'generationDateAndTime="{FIXED_GENERATION_TIMESTAMP}"',
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")
    return path
