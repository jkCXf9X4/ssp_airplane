include(CMakeParseArguments)

function(add_modelica_fmu)
  set(options)
  set(one_value_args TARGET MODEL OUTPUT_NAME)
  set(multi_value_args PACKAGE_FILES DEPENDS)
  cmake_parse_arguments(AMF "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})

  if(NOT AMF_TARGET OR NOT AMF_MODEL OR NOT AMF_OUTPUT_NAME OR NOT AMF_PACKAGE_FILES)
    message(FATAL_ERROR "add_modelica_fmu requires TARGET, MODEL, OUTPUT_NAME, and PACKAGE_FILES")
  endif()

  if(NOT Python3_EXECUTABLE)
    message(FATAL_ERROR "Python3 is required before calling add_modelica_fmu")
  endif()
  if(NOT OMC_EXECUTABLE)
    message(FATAL_ERROR "OMC_EXECUTABLE is required before calling add_modelica_fmu")
  endif()

  set(output_fmu "${CMAKE_BINARY_DIR}/fmus/${AMF_OUTPUT_NAME}.fmu")
  set(work_dir "${CMAKE_BINARY_DIR}/tmp/${AMF_TARGET}")
  set(package_args "")
  foreach(package_file IN LISTS AMF_PACKAGE_FILES)
    list(APPEND package_args "--package-file" "${package_file}")
  endforeach()

  add_custom_command(
    OUTPUT "${output_fmu}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${CMAKE_BINARY_DIR}/fmus"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${work_dir}"
    COMMAND "${Python3_EXECUTABLE}" -m scripts.generation.build_modelica_fmu
            "--omc-path" "${OMC_EXECUTABLE}"
            "--model" "${AMF_MODEL}"
            "--output" "${output_fmu}"
            "--work-dir" "${work_dir}"
            ${package_args}
    DEPENDS
            "${PROJECT_SOURCE_DIR}/scripts/generation/build_modelica_fmu.py"
            ${AMF_PACKAGE_FILES}
            ${AMF_DEPENDS}
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    COMMAND_EXPAND_LISTS
    VERBATIM
  )

  add_custom_target("${AMF_TARGET}" DEPENDS "${output_fmu}")
endfunction()
