if(NOT DEFINED SSD_PATH OR NOT DEFINED FMU_DIR OR NOT DEFINED OUTPUT_PATH OR NOT DEFINED STAGE_DIR)
  message(FATAL_ERROR "SSD_PATH, FMU_DIR, OUTPUT_PATH, and STAGE_DIR are required")
endif()

file(READ "${SSD_PATH}" ssd_contents)
string(REGEX MATCHALL "source=\"resources/[^\"]+\\.fmu\"" source_matches "${ssd_contents}")

if(NOT source_matches)
  message(FATAL_ERROR "No FMU resources referenced by ${SSD_PATH}")
endif()

file(REMOVE_RECURSE "${STAGE_DIR}")
get_filename_component(output_parent "${OUTPUT_PATH}" DIRECTORY)
file(MAKE_DIRECTORY "${output_parent}")
file(MAKE_DIRECTORY "${STAGE_DIR}/resources")
file(COPY_FILE "${SSD_PATH}" "${STAGE_DIR}/SystemStructure.ssd")

set(resource_roots
  "${FMU_DIR}"
  "${FMU_DIR}/cmake/fmus"
)

foreach(source_match IN LISTS source_matches)
  string(REGEX REPLACE "^source=\"(resources/[^\"]+\\.fmu)\"$" "\\1" resource_path "${source_match}")
  get_filename_component(resource_name "${resource_path}" NAME)

  set(found_fmu "")
  foreach(resource_root IN LISTS resource_roots)
    set(candidate "${resource_root}/${resource_name}")
    if(EXISTS "${candidate}")
      set(found_fmu "${candidate}")
      break()
    endif()
  endforeach()

  if(NOT found_fmu)
    message(FATAL_ERROR "Missing FMU referenced by SSD: ${resource_path}")
  endif()

  file(COPY_FILE "${found_fmu}" "${STAGE_DIR}/${resource_path}")
endforeach()

file(REMOVE "${OUTPUT_PATH}")
execute_process(
  COMMAND "${CMAKE_COMMAND}" -E tar cf "${OUTPUT_PATH}" --format=zip "SystemStructure.ssd" "resources"
  WORKING_DIRECTORY "${STAGE_DIR}"
  COMMAND_ERROR_IS_FATAL ANY
)
