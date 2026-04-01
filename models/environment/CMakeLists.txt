add_modelica_fmu(
  TARGET environment_fmu
  MODEL EnvironmentFMU.Environment
  OUTPUT_NAME Aircraft_Environment
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/environment/modelica/EnvironmentFMU/package.mo"
)
