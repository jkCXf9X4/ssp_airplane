cmake_minimum_required(VERSION 3.16)

project(FlightGearBridgeFMU LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(FlightGearBridge SHARED
  src/BridgeRuntime.cpp
  src/FlightGearBridge.cpp
)
set_target_properties(FlightGearBridge PROPERTIES
  PREFIX ""
  OUTPUT_NAME "FlightGearBridge"
)

set(AIRPLANE_REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../..")

target_include_directories(FlightGearBridge PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  ${AIRPLANE_REPO_ROOT}/generated/interfaces
  ${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers
)

target_compile_options(FlightGearBridge PRIVATE -Wall -Wextra -Wpedantic)
