include(CMakeParseArguments)

function(add_native_fmu_package)
  set(options)
  set(one_value_args
    TARGET
    LIBRARY_TARGET
    OUTPUT_NAME
    MODEL_DESCRIPTION
    GENERATED_COMMON_HEADER
    GENERATED_MODEL_HEADER
  )
  cmake_parse_arguments(ANF "${options}" "${one_value_args}" "" ${ARGN})

  if(
    NOT ANF_TARGET
    OR NOT ANF_LIBRARY_TARGET
    OR NOT ANF_OUTPUT_NAME
    OR NOT ANF_MODEL_DESCRIPTION
    OR NOT ANF_GENERATED_COMMON_HEADER
    OR NOT ANF_GENERATED_MODEL_HEADER
  )
    message(FATAL_ERROR "add_native_fmu_package requires all declared arguments")
  endif()

  if(NOT DEFINED AIRPLANE_FMU_OUTPUT_DIR OR NOT DEFINED AIRPLANE_REPO_ROOT)
    message(FATAL_ERROR "AIRPLANE_FMU_OUTPUT_DIR and AIRPLANE_REPO_ROOT must be defined")
  endif()

  if(NOT PYFMI_EXECUTABLE)
    message(FATAL_ERROR
      "PYFMI_EXECUTABLE is required before calling add_native_fmu_package "
      "(configure with -DPYFMI_EXECUTABLE=/path/to/pyfmi)")
  endif()

  set(output_fmu "${AIRPLANE_FMU_OUTPUT_DIR}/${ANF_OUTPUT_NAME}")

  # pyfmi package validates that the binary stem equals the modelIdentifier
  # declared by the model description, then writes a deterministic .fmu.
  # All headers are flattened into sources/ inside the archive; no consumer
  # depends on the previous sources/generated | sources/include layout.
  add_custom_command(
    OUTPUT "${output_fmu}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${AIRPLANE_FMU_OUTPUT_DIR}"
    COMMAND "${PYFMI_EXECUTABLE}" package
      -o "${output_fmu}"
      --model-description "${ANF_MODEL_DESCRIPTION}"
      --binary "$<TARGET_FILE:${ANF_LIBRARY_TARGET}>"
      --header "${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers/fmi2TypesPlatform.h"
      --header "${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers/fmi2FunctionTypes.h"
      --header "${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers/fmi2Functions.h"
      --header "${ANF_GENERATED_COMMON_HEADER}"
      --header "${ANF_GENERATED_MODEL_HEADER}"
    DEPENDS
      "${ANF_LIBRARY_TARGET}"
      "${ANF_MODEL_DESCRIPTION}"
      "${ANF_GENERATED_COMMON_HEADER}"
      "${ANF_GENERATED_MODEL_HEADER}"
    VERBATIM
  )

  add_custom_target("${ANF_TARGET}" DEPENDS "${output_fmu}")
endfunction()
