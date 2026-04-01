include(CMakeParseArguments)

function(add_ssp_package)
  set(options)
  set(one_value_args TARGET SSD OUTPUT_NAME FMU_DIR)
  set(multi_value_args DEPENDS)
  cmake_parse_arguments(ASP "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})

  if(NOT ASP_TARGET OR NOT ASP_SSD OR NOT ASP_OUTPUT_NAME OR NOT ASP_FMU_DIR)
    message(FATAL_ERROR "add_ssp_package requires TARGET, SSD, OUTPUT_NAME, and FMU_DIR")
  endif()

  if(NOT DEFINED AIRPLANE_SSP_OUTPUT_DIR OR NOT DEFINED AIRPLANE_TMP_DIR)
    message(FATAL_ERROR "AIRPLANE_SSP_OUTPUT_DIR and AIRPLANE_TMP_DIR must be defined")
  endif()

  set(output_ssp "${AIRPLANE_SSP_OUTPUT_DIR}/${ASP_OUTPUT_NAME}")
  set(stage_dir "${AIRPLANE_TMP_DIR}/${ASP_TARGET}_stage")

  add_custom_command(
    OUTPUT "${output_ssp}"
    COMMAND "${CMAKE_COMMAND}"
      -DSSD_PATH="${ASP_SSD}"
      -DFMU_DIR="${ASP_FMU_DIR}"
      -DOUTPUT_PATH="${output_ssp}"
      -DSTAGE_DIR="${stage_dir}"
      -P "${CMAKE_CURRENT_FUNCTION_LIST_DIR}/PackageSsp.cmake"
    DEPENDS
      "${ASP_SSD}"
      ${ASP_DEPENDS}
    VERBATIM
  )

  add_custom_target("${ASP_TARGET}" DEPENDS "${output_ssp}")
endfunction()
