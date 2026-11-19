cmake_minimum_required(VERSION 3.16)

project(UdpBridgeFMU LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(UdpBridge SHARED
  src/BridgeRuntime.cpp
  ${AIRPLANE_REPO_ROOT}/generated/interfaces/Aircraft_UdpBridge_fmi.cpp
  ${AIRPLANE_REPO_ROOT}/generated/interfaces/Aircraft_UdpBridge_model.cpp
)
set_target_properties(UdpBridge PROPERTIES
  PREFIX ""
  OUTPUT_NAME "UdpBridge"
)

target_include_directories(UdpBridge PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  ${AIRPLANE_REPO_ROOT}/generated/interfaces
)

target_compile_options(UdpBridge PRIVATE -Wall -Wextra -Wpedantic)

add_native_fmu_package(
  TARGET UdpBridge_fmu
  LIBRARY_TARGET UdpBridge
  OUTPUT_NAME UdpBridge.fmu
  MODEL_DESCRIPTION ${AIRPLANE_REPO_ROOT}/generated/model_descriptions/UdpBridge/modelDescription.xml
  GENERATED_COMMON_HEADER ${AIRPLANE_REPO_ROOT}/generated/interfaces/Aircraft_InterfaceCommon.h
  GENERATED_MODEL_HEADER ${AIRPLANE_REPO_ROOT}/generated/interfaces/Aircraft_UdpBridge.h
)
