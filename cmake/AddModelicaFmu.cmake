include(CMakeParseArguments)

function(add_modelica_fmu)
  set(options)
  set(one_value_args TARGET MODEL OUTPUT_NAME)
  set(multi_value_args PACKAGE_FILES DEPENDS)
  cmake_parse_arguments(AMF "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})

  if(NOT AMF_TARGET OR NOT AMF_MODEL OR NOT AMF_OUTPUT_NAME OR NOT AMF_PACKAGE_FILES)
    message(FATAL_ERROR "add_modelica_fmu requires TARGET, MODEL, OUTPUT_NAME, and PACKAGE_FILES")
  endif()

  if(NOT OMC_EXECUTABLE)
    message(FATAL_ERROR "OMC_EXECUTABLE is required before calling add_modelica_fmu")
  endif()

  string(REGEX REPLACE "^.*\\." "" model_class "${AMF_MODEL}")
  set(output_fmu "${CMAKE_BINARY_DIR}/fmus/${AMF_OUTPUT_NAME}.fmu")
  set(work_dir "${CMAKE_BINARY_DIR}/tmp/${AMF_TARGET}")
  set(mos_file "${CMAKE_BINARY_DIR}/tmp/${AMF_TARGET}.mos")
  set(load_lines "")
  set(package_deps "")

  foreach(package_file IN LISTS AMF_PACKAGE_FILES)
    string(APPEND load_lines "loadFile(\"${package_file}\");\n")
    get_filename_component(package_dir "${package_file}" DIRECTORY)
    file(GLOB_RECURSE package_dir_files CONFIGURE_DEPENDS
      "${package_dir}/*.mo"
      "${package_dir}/*.mos"
      "${package_dir}/package.order"
    )
    list(APPEND package_deps ${package_dir_files})
  endforeach()
  list(REMOVE_DUPLICATES package_deps)

  file(GENERATE OUTPUT "${mos_file}" CONTENT
"installPackage(Modelica, \"4.0.0\", exactMatch=false);
${load_lines}cd(\"${work_dir}\");
setCommandLineOptions(\"--fmiFlags=s:cvode\");
setCommandLineOptions(\"--fmuRuntimeDepends=all\");
filename := OpenModelica.Scripting.buildModelFMU(${AMF_MODEL}, version=\"2.0\", fmuType=\"cs\", platforms={\"static\"});
filename;
getErrorString();
")

  add_custom_command(
    OUTPUT "${output_fmu}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${CMAKE_BINARY_DIR}/fmus"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${work_dir}"
    COMMAND "${OMC_EXECUTABLE}" "${mos_file}"
    COMMAND "${CMAKE_COMMAND}" -E rm -f "${output_fmu}"
    COMMAND "${CMAKE_COMMAND}" -E rename "${work_dir}/${model_class}.fmu" "${output_fmu}"
    DEPENDS
            "${mos_file}"
            ${package_deps}
            ${AMF_DEPENDS}
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    VERBATIM
  )

  add_custom_target("${AMF_TARGET}" DEPENDS "${output_fmu}")
endfunction()
