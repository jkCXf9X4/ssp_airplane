add_modelica_fmu(
  TARGET fuel_system_fmu
  MODEL FuelSystemFMU.FuelSystem
  OUTPUT_NAME Aircraft_FuelSystem
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/fuel_system/modelica/FuelSystemFMU/package.mo"
)
