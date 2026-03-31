set(output_fmu "${CMAKE_BINARY_DIR}/fmus/FlightGearBridge.fmu")
set(native_build_dir "${CMAKE_BINARY_DIR}/native/flightgear_bridge")

add_custom_command(
  OUTPUT "${output_fmu}"
  COMMAND "${CMAKE_COMMAND}" -E make_directory "${CMAKE_BINARY_DIR}/fmus"
  COMMAND "${Python3_EXECUTABLE}" -m scripts.cli.artifacts build-flightgear-bridge-fmu
          "--output" "${output_fmu}"
          "--build-dir" "${native_build_dir}"
  DEPENDS
          "${PROJECT_SOURCE_DIR}/scripts/cli/artifacts.py"
          "${PROJECT_SOURCE_DIR}/scripts/lib/artifacts/build/native_fmus.py"
          "${PROJECT_SOURCE_DIR}/scripts/lib/artifacts/package/native_fmu.py"
          "${PROJECT_SOURCE_DIR}/models/flightgear_bridge/native/CMakeLists.txt"
  WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
  VERBATIM
)

add_custom_target(flightgear_bridge_fmu DEPENDS "${output_fmu}")
