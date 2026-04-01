add_modelica_fmu(
  TARGET composite_airframe_fmu
  MODEL CompositeAirframeFMU.CompositeAirframe
  OUTPUT_NAME CompositeAirframe
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/composite_airframe/modelica/CompositeAirframeFMU/package.mo"
)
