cmake_minimum_required(VERSION 3.16)

project(ssp_airplane LANGUAGES CXX)

set(AIRPLANE_REPO_ROOT "${PROJECT_SOURCE_DIR}")
set(AIRPLANE_BUILD_ROOT "${PROJECT_SOURCE_DIR}/build")
set(AIRPLANE_FMU_OUTPUT_DIR "${AIRPLANE_BUILD_ROOT}/fmus")
set(AIRPLANE_SSP_OUTPUT_DIR "${AIRPLANE_BUILD_ROOT}/ssp")
set(AIRPLANE_TMP_DIR "${AIRPLANE_BUILD_ROOT}/tmp")
set(AIRPLANE_SSD_PATH "${PROJECT_SOURCE_DIR}/generated/SystemStructure.ssd")

find_program(OMC_EXECUTABLE omc)

if(NOT OMC_EXECUTABLE)
  message(FATAL_ERROR "Could not find omc. Install OpenModelica or set OMC_EXECUTABLE.")
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(AddModelicaFmu)
include(AddNativeFmu)
include(AddSspPackage)

add_subdirectory(models/flightgear_bridge)
add_subdirectory(models/adaptive_wing_system)
add_subdirectory(models/autopilot_module)
add_subdirectory(models/composite_airframe)
add_subdirectory(models/control_interface)
add_subdirectory(models/environment)
add_subdirectory(models/fuel_system)
add_subdirectory(models/input_output)
add_subdirectory(models/mission_computer)
add_subdirectory(models/turbofan_propulsion)

add_custom_target(build_fmus ALL
  DEPENDS
    FlightGearBridge_fmu
    adaptive_wing_system_fmu
    autopilot_module_fmu
    composite_airframe_fmu
    control_interface_fmu
    environment_fmu
    fuel_system_fmu
    input_output_fmu
    mission_computer_fmu
    turbofan_propulsion_fmu
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
