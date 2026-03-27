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

target_include_directories(FlightGearBridge PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  /home/eriro/pwa/2_work/ssp4sim/3rdParty/fmi4c/3rdparty/fmi
)

target_compile_definitions(FlightGearBridge PRIVATE FMI2_FUNCTION_PREFIX=FlightGearBridge_)

target_compile_options(FlightGearBridge PRIVATE -Wall -Wextra -Wpedantic)
