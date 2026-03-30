add_modelica_fmu(
  TARGET turbofan_propulsion_fmu
  MODEL TurbofanPropulsionFMU.TurbofanPropulsion
  OUTPUT_NAME Aircraft_TurbofanPropulsion
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/models/common/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/turbofan_propulsion/modelica/TurbofanPropulsionFMU/package.mo"
)
