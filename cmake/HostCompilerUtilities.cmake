# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

include(CMakeParseArguments)

macro(load_host_compiler_preferences lang)
  include(${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION}/CMakeHOST${lang}Compiler.cmake OPTIONAL)
endmacro(load_host_compiler_preferences)

function(save_host_compiler_preferences lang)
  # Set internal directory path if missing
  if(NOT CMAKE_PLATFORM_INFO_DIR)
    set(CMAKE_PLATFORM_INFO_DIR ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION})
  endif()

  file(WRITE ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake.in
    "set(CMAKE_HOST${lang}_COMPILER \"@CMAKE_HOST${lang}_COMPILER@\")\n"
    "set(CMAKE_HOST${lang}_COMPILER_ID \"@CMAKE_HOST${lang}_COMPILER_ID@\")\n"
    "set(CMAKE_HOST${lang}_COMPILER_VERSION \"@CMAKE_HOST${lang}_COMPILER_VERSION@\")\n"
    "set(CMAKE_HOST${lang}_COMPILER_WORKS @CMAKE_HOST${lang}_COMPILER_WORKS@)\n"
    "set(CMAKE_HOST${lang}_STANDARD_COMPUTED_DEFAULT \"@CMAKE_HOST${lang}_STANDARD_COMPUTED_DEFAULT@\")\n"
    "set(CMAKE_HOST${lang}_PLATFORM_ID \"@CMAKE_HOST${lang}_PLATFORM_ID@\")\n"
    "set(CMAKE_HOST${lang}_ABI_COMPILED @CMAKE_HOST${lang}_ABI_COMPILED@)\n"
    "set(CMAKE_HOST${lang}_COMPILER_ABI \"@CMAKE_HOST${lang}_COMPILER_ABI@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES \"@CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES \"@CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES \"@CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES \"@CMAKE_HOST${lang}_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES@\")\n"
    "set(CMAKE_HOST${lang}_VERBOSE_FLAG \"@CMAKE_HOST${lang}_VERBOSE_FLAG@\")\n"
    "set(CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang} \"@CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang}@\")\n"
  )

  # Guess the supported language standard versions based on C and CXX
  list(APPEND versions 90 98 99 03 11 14 17 20 23 26)

  foreach(version IN LISTS versions)
    if(CMAKE_HOST${lang}${version}_STANDARD_COMPILE_OPTION)
      file(APPEND ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake.in
        "set(CMAKE_HOST${lang}${version}_STANDARD_COMPILE_OPTION \"@CMAKE_HOST${lang}${version}_STANDARD_COMPILE_OPTION@\")\n"
      )
    endif()
    if(CMAKE_HOST${lang}${version}_EXTENSION_COMPILE_OPTION)
      file(APPEND ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake.in
        "set(CMAKE_HOST${lang}${version}_EXTENSION_COMPILE_OPTION \"@CMAKE_HOST${lang}${version}_EXTENSION_COMPILE_OPTION@\")\n"
      )
    endif()
  endforeach()

  configure_file(
    ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake.in
    ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake
    @ONLY
  )
endfunction(save_host_compiler_preferences)

function(find_host_compiler lang)
  include(CMakeDetermineCompiler)
  _cmake_find_compiler(HOST${lang})
  mark_as_advanced(CMAKE_HOST${lang}_COMPILER)
endfunction(find_host_compiler)

function(find_host_compiler_id lang)
  set(multiValueArgs FLAGS)
  cmake_parse_arguments(TEST "" "" "${multiValueArgs}" ${ARGN})

  # Try to use the CMake internal compiler detection routines.
  # Use the CMake_${lang}_* variables to make the routines work.
  set(CMAKE_${lang}_COMPILER "${CMAKE_HOST${lang}_COMPILER}")
  set(CMAKE_${lang}_COMPILER_ID_TEST_FLAGS_FIRST)
  set(CMAKE_${lang}_COMPILER_ID_TEST_FLAGS "${TEST_FLAGS}")

  # Try to identify the compiler.
  set(CMAKE_${lang}_FLAGS)
  set(CMAKE_${lang}_COMPILER_ID)
  set(CMAKE_${lang}_PLATFORM_ID)

  file(READ ${CMAKE_ROOT}/Modules/CMakePlatformId.h.in CMAKE_${lang}_COMPILER_ID_PLATFORM_CONTENT)

  set(CMAKE_${lang}_COMPILER_ID_TOOL_MATCH_REGEX "\nLd[^\n]*(\n[ \t]+[^\n]*)*\n[ \t]+([^ \t\r\n]+)[^\r\n]*-o[^\r\n]*CompilerId${lang}/(\\./)?(CompilerId${lang}.(framework|xctest)/)?CompilerId${lang}[ \t\n\\\"]")
  set(CMAKE_${lang}_COMPILER_ID_TOOL_MATCH_INDEX 2)

  # Set internal directory path if missing
  if(NOT CMAKE_PLATFORM_INFO_DIR)
    set(CMAKE_PLATFORM_INFO_DIR ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION})
  endif()

  # Copy the original file to temporary directory
  configure_file(
    ${CMAKE_ROOT}/Modules/CMake${lang}CompilerId.c.in
    ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}CompilerId.c.in
    COPYONLY
  )

  # Add the location of the above file to the module path
  set(_cmake_module_path ${CMAKE_MODULE_PATH})
  list(APPEND CMAKE_MODULE_PATH ${CMAKE_PLATFORM_INFO_DIR})

  # Try to identify the compiler information
  include(CMakeDetermineCompilerId)
  CMAKE_DETERMINE_COMPILER_ID(${lang} HOST${lang}FLAGS CMakeHOST${lang}CompilerId.c)

  # Restore the original module path
  set(CMAKE_MODULE_PATH ${_cmake_module_path})

  # Load compiler-specific information
  if(CMAKE_${lang}_COMPILER_ID)
    include(Compiler/${CMAKE_${lang}_COMPILER_ID}-${lang} OPTIONAL)
  endif()

  # Set host compiler-specific information
  set(CMAKE_HOST${lang}_COMPILER_ID "${CMAKE_${lang}_COMPILER_ID}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_COMPILER_VERSION "${CMAKE_${lang}_COMPILER_VERSION}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_PLATFORM_ID "${CMAKE_${lang}_PLATFORM_ID}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_STANDARD_COMPUTED_DEFAULT "${CMAKE_${lang}_STANDARD_COMPUTED_DEFAULT}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_VERBOSE_FLAG "${CMAKE_${lang}_VERBOSE_FLAG}" PARENT_SCOPE)
  set(CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang} "${CMAKE_INCLUDE_SYSTEM_FLAG_${lang}}" PARENT_SCOPE)

  # Guess the supported language standard versions based on C and CXX
  list(APPEND versions 90 98 99 03 11 14 17 20 23 26)

  # Set standard compile options
  foreach(version IN LISTS versions)
    if(CMAKE_${lang}${version}_STANDARD_COMPILE_OPTION)
      set(CMAKE_HOST${lang}${version}_STANDARD_COMPILE_OPTION "${CMAKE_${lang}${version}_STANDARD_COMPILE_OPTION}" PARENT_SCOPE)
    endif()
    if(CMAKE_${lang}${version}_EXTENSION_COMPILE_OPTION)
      set(CMAKE_HOST${lang}${version}_EXTENSION_COMPILE_OPTION "${CMAKE_${lang}${version}_EXTENSION_COMPILE_OPTION}" PARENT_SCOPE)
    endif()
  endforeach()
endfunction(find_host_compiler_id)

function(try_host_compile lang)
  set(oneValueArgs SOURCE TARGET WORKING_DIRECTORY RESULT_VARIABLE OUTPUT_VARIABLE)
  set(multiValueArgs COMPILE_OPTIONS)

  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  file(REMOVE ${BUILD_TARGET})

  execute_process(
    COMMAND ${CMAKE_HOST${lang}_COMPILER} ${BUILD_COMPILE_OPTIONS} ${BUILD_SOURCE} -o ${BUILD_TARGET}
    WORKING_DIRECTORY ${BUILD_WORKING_DIRECTORY}
    RESULT_VARIABLE RESULT
    OUTPUT_VARIABLE OUTPUT
    ERROR_VARIABLE OUTPUT
    ERROR_QUIET
  )

  if(RESULT EQUAL 0)
    set(${BUILD_RESULT_VARIABLE} TRUE PARENT_SCOPE)
  endif()

  set(${BUILD_OUTPUT_VARIABLE} ${OUTPUT} PARENT_SCOPE)
endfunction(try_host_compile)

function(parse_host_compiler_abi_info lang bin)
  file(STRINGS "${bin}" ABI_STRINGS REGEX "INFO:[A-Za-z0-9_]+\\[[^]]*\\]")
  foreach(info ${ABI_STRINGS})
    if("${info}" MATCHES "INFO:abi\\[([^]]*)\\]")
      set(CMAKE_HOST${lang}_COMPILER_ABI "${CMAKE_MATCH_1}" PARENT_SCOPE)
      break()
    endif()
  endforeach()
endfunction(parse_host_compiler_abi_info)

function(parse_host_implicit_include_info lang text)
  include(CMakeParseImplicitIncludeInfo)

  set(implicit_incdirs "")

  cmake_parse_implicit_include_info("${text}" HOST${lang} implicit_incdirs log rv)

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Parsed HOST${lang} implicit include dir info from above output: rv=${rv}\n${log}\n\n")

  set(CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES "${implicit_incdirs}" PARENT_SCOPE)
endfunction(parse_host_implicit_include_info)

function(parse_host_implicit_link_info lang text)
  include(CMakeParseImplicitLinkInfo)

  set(implicit_libs "")
  set(implicit_dirs "")
  set(implicit_fwks "")

  CMAKE_PARSE_IMPLICIT_LINK_INFO("${text}" implicit_libs implicit_dirs implicit_fwks log "${CMAKE_HOST${lang}_IMPLICIT_OBJECT_REGEX}")

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Parsed HOST${lang} implicit link information from above output:\n${log}\n\n"
  )

  set(CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES "${implicit_libs}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES "${implicit_dirs}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_IMPLICIT_FRAMEWORK_DIRECTORIES "${implicit_fwks}" PARENT_SCOPE)
endfunction(parse_host_implicit_link_info)
