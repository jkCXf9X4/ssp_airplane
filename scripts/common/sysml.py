"""Compatibility helpers for the extracted SysML package surface."""
from __future__ import annotations

from typing import List

from pycps_sysmlv2 import (
    SysMLArchitecture,
)


def select_parts(architecture: SysMLArchitecture, parts: List[str]):
    return [x for x in architecture.part_definitions.values() if x.name in parts]

