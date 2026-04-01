add_modelica_fmu(
  TARGET autopilot_module_fmu
  MODEL AutopilotModuleFMU.AutopilotModule
  OUTPUT_NAME AutopilotModule
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/autopilot_module/modelica/AutopilotModuleFMU/package.mo"
)
