"""Registry for standalone Modelica FMU packages."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from scripts.common.paths import COMMON_MODEL_DIR, MODELS_DIR


@dataclass(frozen=True)
class ModelicaModelSpec:
    folder_name: str
    package_name: str
    class_name: str
    output_name: str

    @property
    def package_file(self) -> Path:
        return MODELS_DIR / self.folder_name / "modelica" / self.package_name / "package.mo"

    @property
    def model_file(self) -> Path:
        return MODELS_DIR / self.folder_name / "modelica" / self.package_name / f"{self.class_name}.mo"

    @property
    def model_name(self) -> str:
        return f"{self.package_name}.{self.class_name}"

    @property
    def package_files(self) -> list[Path]:
        return [COMMON_PACKAGE_FILE, self.package_file]


COMMON_PACKAGE_FILE = COMMON_MODEL_DIR / "modelica" / "AircraftCommon" / "package.mo"

MODELICA_MODEL_SPECS = [
    ModelicaModelSpec("adaptive_wing_system", "AdaptiveWingSystemFMU", "AdaptiveWingSystem", "Aircraft_AdaptiveWingSystem"),
    ModelicaModelSpec("autopilot_module", "AutopilotModuleFMU", "AutopilotModule", "Aircraft_AutopilotModule"),
    ModelicaModelSpec("composite_airframe", "CompositeAirframeFMU", "CompositeAirframe", "Aircraft_CompositeAirframe"),
    ModelicaModelSpec("control_interface", "ControlInterfaceFMU", "ControlInterface", "Aircraft_ControlInterface"),
    ModelicaModelSpec("environment", "EnvironmentFMU", "Environment", "Aircraft_Environment"),
    ModelicaModelSpec("fuel_system", "FuelSystemFMU", "FuelSystem", "Aircraft_FuelSystem"),
    ModelicaModelSpec("input_output", "InputOutputFMU", "InputOutput", "Aircraft_InputOutput"),
    ModelicaModelSpec("mission_computer", "MissionComputerFMU", "MissionComputer", "Aircraft_MissionComputer"),
    ModelicaModelSpec("turbofan_propulsion", "TurbofanPropulsionFMU", "TurbofanPropulsion", "Aircraft_TurbofanPropulsion"),
]

DEFAULT_MODELICA_MODELS = [spec.model_name for spec in MODELICA_MODEL_SPECS]


def spec_by_model_name(model_name: str) -> ModelicaModelSpec:
    for spec in MODELICA_MODEL_SPECS:
        if spec.model_name == model_name:
            return spec
    raise KeyError(model_name)
