add_modelica_fmu(
  TARGET mission_computer_fmu
  MODEL MissionComputerFMU.MissionComputer
  OUTPUT_NAME MissionComputer
  PACKAGE_FILES
    "${PROJECT_SOURCE_DIR}/generated/modelica/AircraftCommon/package.mo"
    "${PROJECT_SOURCE_DIR}/models/mission_computer/modelica/MissionComputerFMU/package.mo"
)
