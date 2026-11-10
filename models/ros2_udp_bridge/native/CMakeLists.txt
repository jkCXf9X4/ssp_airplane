cmake_minimum_required(VERSION 3.16)

project(Ros2UdpBridgeFMU LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(Ros2UdpBridge SHARED
  src/BridgeRuntime.cpp
  src/Ros2UdpBridge.cpp
)
set_target_properties(Ros2UdpBridge PROPERTIES
  PREFIX ""
  OUTPUT_NAME "Ros2UdpBridge"
)

set(AIRPLANE_REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../..")

target_include_directories(Ros2UdpBridge PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  ${AIRPLANE_REPO_ROOT}/generated/interfaces
  ${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers
)

target_compile_options(Ros2UdpBridge PRIVATE -Wall -Wextra -Wpedantic)

add_native_fmu_package(
  TARGET Ros2UdpBridge_fmu
  LIBRARY_TARGET Ros2UdpBridge
  OUTPUT_NAME Ros2UdpBridge.fmu
  MODEL_DESCRIPTION ${AIRPLANE_REPO_ROOT}/generated/model_descriptions/Ros2UdpBridge/modelDescription.xml
  GENERATED_COMMON_HEADER ${AIRPLANE_REPO_ROOT}/generated/interfaces/Aircraft_InterfaceCommon.h
  GENERATED_MODEL_HEADER ${AIRPLANE_REPO_ROOT}/generated/interfaces/Aircraft_Ros2UdpBridge.h
)
