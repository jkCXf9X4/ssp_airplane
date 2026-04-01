add_modelica_fmu(
  TARGET control_interface_fmu
  MODEL ControlInterfaceFMU.ControlInterface
  OUTPUT_NAME ControlInterface
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/control_interface/modelica/ControlInterfaceFMU/package.mo"
)
