cmake_minimum_required(VERSION 3.16)

project(ssp_airplane LANGUAGES CXX)

# All build outputs must live under build/. Configure out-of-source only:
#   cmake -S . -B build/cmake
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
  message(FATAL_ERROR
    "In-source builds are not allowed; they would pollute the source tree.\n"
    "Configure out-of-source instead:\n"
    "  cmake -S . -B build/cmake")
endif()


set(AIRPLANE_REPO_ROOT "${PROJECT_SOURCE_DIR}")
set(AIRPLANE_BUILD_ROOT "${PROJECT_SOURCE_DIR}/build")
set(AIRPLANE_FMU_OUTPUT_DIR "${AIRPLANE_BUILD_ROOT}/fmus")
set(AIRPLANE_SSP_OUTPUT_DIR "${AIRPLANE_BUILD_ROOT}/ssp")
set(AIRPLANE_TMP_DIR "${AIRPLANE_BUILD_ROOT}/tmp")
set(AIRPLANE_SSD_PATH "${PROJECT_SOURCE_DIR}/generated/SystemStructure.ssd")

find_program(PYFMI_EXECUTABLE pyfmi
  HINTS "${PROJECT_SOURCE_DIR}/../../../venv/bin"
)
if(NOT PYFMI_EXECUTABLE)
  message(FATAL_ERROR
    "Could not find pyfmi. Install pyfmi_sysml2 or set PYFMI_EXECUTABLE.")
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(AddNativeFmu)
include(AddSspPackage)

# The standalone Modelica FMUs are built by scripts.lib.common.modelica.
add_subdirectory(models/flightgear_bridge)

add_custom_target(build_fmus ALL
  DEPENDS
    FlightGearBridge_fmu
)

add_ssp_package(
  TARGET aircraft_ssp
  SSD "${AIRPLANE_SSD_PATH}"
  FMU_DIR "${AIRPLANE_FMU_OUTPUT_DIR}"
  OUTPUT_NAME "aircraft.ssp"
  DEPENDS build_fmus
)

add_custom_target(package_simulation_artifacts ALL
  DEPENDS
    build_fmus
    aircraft_ssp
)
