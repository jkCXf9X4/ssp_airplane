"""Compatibility shim for the extracted SysML parser package."""
from __future__ import annotations

from typing import Any

try:
    from pycps_sysmlv2 import (  # type: ignore
        SysMLArchitecture,
        SysMLPartDefinition,
        SysMLPortDefinition,
        load_architecture as parse_sysml_folder,
    )
except ModuleNotFoundError:
    try:
        from sysml import load_architecture as parse_sysml_folder  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover
        def parse_sysml_folder(*args, **kwargs):
            raise ModuleNotFoundError("Neither pycps_sysmlv2 nor sysml is importable")

    SysMLArchitecture = Any
    SysMLPartDefinition = Any
    SysMLPortDefinition = Any
