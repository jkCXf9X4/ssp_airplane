include(CMakeParseArguments)

function(add_native_fmu_package)
  set(options)
  set(one_value_args
    TARGET
    LIBRARY_TARGET
    MODEL_IDENTIFIER
    OUTPUT_NAME
    SOURCE_DIR
    MODEL_DESCRIPTION
    GENERATED_COMMON_HEADER
    GENERATED_MODEL_HEADER
  )
  cmake_parse_arguments(ANF "${options}" "${one_value_args}" "" ${ARGN})

  if(
    NOT ANF_TARGET
    OR NOT ANF_LIBRARY_TARGET
    OR NOT ANF_MODEL_IDENTIFIER
    OR NOT ANF_OUTPUT_NAME
    OR NOT ANF_SOURCE_DIR
    OR NOT ANF_MODEL_DESCRIPTION
    OR NOT ANF_GENERATED_COMMON_HEADER
    OR NOT ANF_GENERATED_MODEL_HEADER
  )
    message(FATAL_ERROR "add_native_fmu_package requires all declared arguments")
  endif()

  if(NOT DEFINED AIRPLANE_FMU_OUTPUT_DIR OR NOT DEFINED AIRPLANE_TMP_DIR OR NOT DEFINED AIRPLANE_REPO_ROOT)
    message(FATAL_ERROR "AIRPLANE_FMU_OUTPUT_DIR, AIRPLANE_TMP_DIR, and AIRPLANE_REPO_ROOT must be defined")
  endif()

  get_filename_component(common_header_name "${ANF_GENERATED_COMMON_HEADER}" NAME)
  get_filename_component(model_header_name "${ANF_GENERATED_MODEL_HEADER}" NAME)
  set(output_fmu "${AIRPLANE_FMU_OUTPUT_DIR}/${ANF_OUTPUT_NAME}")
  set(stage_dir "${AIRPLANE_TMP_DIR}/${ANF_TARGET}_stage")

  add_custom_command(
    OUTPUT "${output_fmu}"
    COMMAND "${CMAKE_COMMAND}" -E rm -rf "${stage_dir}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${AIRPLANE_FMU_OUTPUT_DIR}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${stage_dir}/binaries/linux64"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${stage_dir}/sources/generated"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${stage_dir}/sources/include"
    COMMAND "${CMAKE_COMMAND}" -E copy_directory "${ANF_SOURCE_DIR}" "${stage_dir}/sources"
    COMMAND "${CMAKE_COMMAND}" -E copy "$<TARGET_FILE:${ANF_LIBRARY_TARGET}>" "${stage_dir}/binaries/linux64/${ANF_MODEL_IDENTIFIER}.so"
    COMMAND "${CMAKE_COMMAND}" -E copy "${ANF_MODEL_DESCRIPTION}" "${stage_dir}/modelDescription.xml"
    COMMAND "${CMAKE_COMMAND}" -E copy "${ANF_GENERATED_COMMON_HEADER}" "${stage_dir}/sources/generated/${common_header_name}"
    COMMAND "${CMAKE_COMMAND}" -E copy "${ANF_GENERATED_MODEL_HEADER}" "${stage_dir}/sources/generated/${model_header_name}"
    COMMAND "${CMAKE_COMMAND}" -E copy "${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers/fmi2TypesPlatform.h" "${stage_dir}/sources/include/fmi2TypesPlatform.h"
    COMMAND "${CMAKE_COMMAND}" -E copy "${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers/fmi2FunctionTypes.h" "${stage_dir}/sources/include/fmi2FunctionTypes.h"
    COMMAND "${CMAKE_COMMAND}" -E copy "${AIRPLANE_REPO_ROOT}/3rd_party/fmi_headers/fmi2Functions.h" "${stage_dir}/sources/include/fmi2Functions.h"
    COMMAND "${CMAKE_COMMAND}" -E rm -f "${output_fmu}"
    COMMAND "${CMAKE_COMMAND}" -E chdir "${stage_dir}" "${CMAKE_COMMAND}" -E tar "cf" "${output_fmu}" --format=zip "binaries" "modelDescription.xml" "sources"
    DEPENDS
      "${ANF_LIBRARY_TARGET}"
      "${ANF_MODEL_DESCRIPTION}"
      "${ANF_GENERATED_COMMON_HEADER}"
      "${ANF_GENERATED_MODEL_HEADER}"
    VERBATIM
  )

  add_custom_target("${ANF_TARGET}" DEPENDS "${output_fmu}")
endfunction()
