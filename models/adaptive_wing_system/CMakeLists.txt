add_modelica_fmu(
  TARGET adaptive_wing_system_fmu
  MODEL AdaptiveWingSystemFMU.AdaptiveWingSystem
  OUTPUT_NAME Aircraft_AdaptiveWingSystem
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/adaptive_wing_system/modelica/AdaptiveWingSystemFMU/package.mo"
)
