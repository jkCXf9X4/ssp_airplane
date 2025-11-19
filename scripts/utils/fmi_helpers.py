"""Utility helpers for working with FMI artifacts derived from Modelica classes."""
from __future__ import annotations

from typing import Dict

from scripts.utils.sysmlv2_arch_parser import SysMLArchitecture
from scripts.utils.sysml_helpers import component_modelica_map


def fmu_filename(modelica_class: str) -> str:
    """Return the FMU filename for a fully-qualified Modelica class."""
    return modelica_class.replace(".", "_") + ".fmu"


def fmu_resource_path(modelica_class: str) -> str:
    """Return the SSP resources relative path for an FMU."""
    return f"resources/{fmu_filename(modelica_class)}"


def architecture_model_map(architecture: SysMLArchitecture) -> Dict[str, str]:
    """Convenience wrapper to build the part->Modelica class mapping."""
    return component_modelica_map(architecture)


def component_fmu_source(component_name: str, class_map: Dict[str, str]) -> str:
    """Resolve the FMU resource path for a given component."""
    modelica_class = class_map.get(component_name)
    if not modelica_class:
        raise KeyError(f"No Modelica class map defined for component '{component_name}'")
    return fmu_resource_path(modelica_class)
