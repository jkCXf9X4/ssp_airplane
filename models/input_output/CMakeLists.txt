add_modelica_fmu(
  TARGET input_output_fmu
  MODEL InputOutputFMU.InputOutput
  OUTPUT_NAME InputOutput
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/input_output/modelica/InputOutputFMU/package.mo"
)
