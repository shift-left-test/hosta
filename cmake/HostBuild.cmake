# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

set(HOSTA_MAJOR_VERSION 1)
set(HOSTA_MINOR_VERSION 4)
set(HOSTA_PATCH_VERSION 0)
set(HOSTA_VERSION ${HOSTA_MAJOR_VERSION}.${HOSTA_MINOR_VERSION}.${HOSTA_PATCH_VERSION})

# Check the minimum required CMake version
if(CMAKE_VERSION VERSION_LESS "3.17")
  message(FATAL_ERROR "CMake 3.17 or higher is required.  You are running version ${CMAKE_VERSION}\n")
endif()

# Set the directory of the current file
if(NOT _HOSTA_BASE_DIR)
  set(_HOSTA_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")
endif()

include(CMakeParseArguments)
include(${_HOSTA_BASE_DIR}/HostCompilerUtilities.cmake)

# Set the default preferred host languages
if(NOT ENABLE_HOST_LANGUAGES)
  set(ENABLE_HOST_LANGUAGES C CXX)
endif()
list(TRANSFORM ENABLE_HOST_LANGUAGES TOUPPER)
list(REMOVE_DUPLICATES ENABLE_HOST_LANGUAGES)
list(SORT ENABLE_HOST_LANGUAGES)

# Set the list of enabled host languages
unset(ENABLED_HOST_LANGUAGES)
foreach(lang IN LISTS ENABLE_HOST_LANGUAGES)
  if(lang STREQUAL NONE)
    continue()
  elseif(NOT EXISTS "${_HOSTA_BASE_DIR}/DetermineHOST${lang}Compiler.cmake")
    host_logging_error("No CMAKE_HOST${lang}_COMPILER could be found.")
  else()
    include(${_HOSTA_BASE_DIR}/DetermineHOST${lang}Compiler.cmake)
  endif()
endforeach()

# Set default host build target name
if(NOT CMAKE_HOST_BUILD_TARGET)
  set(CMAKE_HOST_BUILD_TARGET "host-targets")
endif()

# Set default host build target
add_custom_target(${CMAKE_HOST_BUILD_TARGET})

# Set host namespace prefix
set(CMAKE_HOST_NAMESPACE_PREFIX "Host::")

# Set host target prefix
set(CMAKE_HOST_TARGET_PREFIX "HOST-")

# Remove the host namespace prefix if exists
function(remove_host_namespace_prefix OUTPUT INPUT)
  unset(_result)
  string(REGEX REPLACE "^${CMAKE_HOST_NAMESPACE_PREFIX}(.*)" "\\1" _result "${INPUT}")
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(remove_host_namespace_prefix)

# Replace the host namespace with the relevant prefix for host target
function(get_host_target_name OUTPUT INPUT)
  unset(_result)
  string(REGEX REPLACE "^${CMAKE_HOST_NAMESPACE_PREFIX}(.*)" "${CMAKE_HOST_TARGET_PREFIX}\\1" _result "${INPUT}")
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(get_host_target_name)

function(get_host_target_names OUTPUT INPUT)
  unset(_result)
  foreach(arg IN LISTS INPUT)
    get_host_target_name(_target "${arg}")
    list(APPEND _result "${_target}")
  endforeach()
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(get_host_target_names)

# Define custom target properties
define_property(TARGET PROPERTY HOST_TYPE
  BRIEF_DOCS "Type of the host target"
  FULL_DOCS "Type of the host target"
)

define_property(TARGET PROPERTY HOST_NAME
  BRIEF_DOCS "Name of the host target"
  FULL_DOCS "Name of the host target"
)

define_property(TARGET PROPERTY HOST_OUTPUT_NAME
  BRIEF_DOCS "Output name of the host target"
  FULL_DOCS "Output name of the host target"
)

define_property(TARGET PROPERTY HOST_SOURCES
  BRIEF_DOCS "List of source files for host targets"
  FULL_DOCS "List of source files for host targets"
)

define_property(TARGET PROPERTY HOST_INTERFACE_INCLUDE_DIRECTORIES
  BRIEF_DOCS "List of include directories for host targets"
  FULL_DOCS "List of include directories for host targets"
)

define_property(TARGET PROPERTY HOST_INTERFACE_COMPILE_OPTIONS
  BRIEF_DOCS "List of compile options for host targets"
  FULL_DOCS "List of compile options for host targets"
)

define_property(TARGET PROPERTY HOST_INTERFACE_LINK_OPTIONS
  BRIEF_DOCS "List of link options for host targets"
  FULL_DOCS "List of link options for host targets"
)

define_property(TARGET PROPERTY HOST_VERSION
  BRIEF_DOCS "Version of the host target"
  FULL_DOCS "Version of the host target"
)

define_property(TARGET PROPERTY HOST_SOVERSION
  BRIEF_DOCS "SO version of the host target"
  FULL_DOCS "SO version of the host target"
)

function(get_host_target_property VARIABLE TARGET PROPERTY)
  get_host_target_name(TARGET "${TARGET}")

  if(NOT TARGET ${TARGET})
    message(FATAL_ERROR "get_host_target_property() called with non-existent target \"${TARGET}\".\n")
  endif()

  # Try fetching host properties first
  unset(_result)
  get_target_property(_result "${TARGET}" "HOST_${PROPERTY}")
  if(NOT _result)
    get_target_property(_result "${TARGET}" "${PROPERTY}")
  endif()
  if(_result)
    set(${VARIABLE} ${_result} PARENT_SCOPE)
  endif()
endfunction(get_host_target_property)

function(get_host_target_properties TARGET)
  set(oneValueArgs NAME OUTPUT_NAME TYPE SOURCE_DIR BINARY_DIR VERSION SOVERSION)
  set(multiValueArgs SOURCES INTERFACE_INCLUDE_DIRECTORIES INTERFACE_COMPILE_OPTIONS INTERFACE_LINK_OPTIONS)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(properties ${oneValueArgs} ${multiValueArgs})
  foreach(property IN LISTS properties)
    if(ARG_${property})
      unset(_result)
      get_host_target_property(_result ${TARGET} ${property})
      set("${ARG_${property}}" ${_result} PARENT_SCOPE)
    endif()
  endforeach()
endfunction(get_host_target_properties)

function(set_host_target_property TARGET PROPERTY VALUE)
  get_host_target_name(TARGET "${TARGET}")

  if(NOT TARGET ${TARGET})
    message(FATAL_ERROR "set_host_target_property() called with non-existent target \"${TARGET}\".\n")
  endif()

  # Try setting host properties first
  unset(_result)
  get_property(_result TARGET "${TARGET}" PROPERTY "HOST_${PROPERTY}" DEFINED)
  if(_result)
    set(PROPERTY "HOST_${PROPERTY}")
  endif()
  set_target_properties(${TARGET} PROPERTIES ${PROPERTY} "${VALUE}")
endfunction(set_host_target_property)

function(set_host_target_properties TARGET)
  set(oneValueArgs NAME OUTPUT_NAME TYPE VERSION SOVERSION)
  set(multiValueArgs SOURCES INTERFACE_INCLUDE_DIRECTORIES INTERFACE_COMPILE_OPTIONS INTERFACE_LINK_OPTIONS)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(properties ${oneValueArgs} ${multiValueArgs})
  foreach(property IN LISTS properties)
    if(ARG_${property})
      set_host_target_property("${TARGET}" "${property}" "${ARG_${property}}")
    endif()
  endforeach()
endfunction(set_host_target_properties)

function(add_host_dependencies TARGET DEPENDENCIES)
  get_host_target_name(TARGET "${TARGET}")
  get_host_target_names(DEPENDENCIES "${DEPENDENCIES}")
  add_dependencies(${TARGET} ${DEPENDENCIES})
endfunction(add_host_dependencies)

function(add_host_custom_target TARGET)
  set(multiValueArgs DEPENDS)
  cmake_parse_arguments(ARG "" "" "${multiValueArgs}" ${ARGN})

  get_host_target_name(TARGET "${TARGET}")

  if(ARG_DEPENDS)
    get_host_target_names(DEPENDENCIES "${ARG_DEPENDS}")
    add_custom_target(${TARGET} DEPENDS ${DEPENDENCIES})
  else()
    add_custom_target(${TARGET})
  endif()
endfunction(add_host_custom_target)

function(transform_host_arguments OUTPUT INPUT)
  set(oneValueArgs PREPEND)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "" ${ARGN})

  unset(_result)
  if(ARG_PREPEND)
    foreach(arg IN LISTS INPUT)
      # Skip generator expressions
      if("${arg}" MATCHES "\\$<")
        list(APPEND _result "${arg}")
      else()
        list(APPEND _result "${ARG_PREPEND}${arg}")
      endif()
    endforeach()
  else()
    set(_result "${INPUT}")
  endif()
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(transform_host_arguments)

function(separate_host_scoped_arguments INPUT OUTPUT INTERFACE_OUTPUT)
  set(_interface_mode FALSE)
  set(_result )
  set(_interface_result )

  if(NOT "${INPUT}" MATCHES "^$|PRIVATE.*|PUBLIC.*")
    host_logging_error("The function called with invalid arguments: '${INPUT}'\nPRIVATE or PUBLIC keywords are required to specify the scope of the arguments.")
  endif()

  while(INPUT)
    list(POP_FRONT INPUT arg)
    if(arg STREQUAL "PRIVATE")
      set(_interface_mode FALSE)
    elseif(arg STREQUAL "PUBLIC")
      set(_interface_mode TRUE)
    else()
      list(APPEND _result "${arg}")
      if(_interface_mode)
        list(APPEND _interface_result "${arg}")
      endif()
    endif()
  endwhile()

  set(${OUTPUT} ${_result} PARENT_SCOPE)
  set(${INTERFACE_OUTPUT} ${_interface_result} PARENT_SCOPE)
endfunction(separate_host_scoped_arguments)

function(get_host_file_dependencies lang OUTPUT)
  set(oneValueArgs SOURCE)
  set(multiValueArgs INCLUDE_DIRECTORIES COMPILE_OPTIONS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Resolve absolute path
  get_filename_component(BUILD_SOURCE ${BUILD_SOURCE} ABSOLUTE)

  # Resolve file dependencies
  set(BUILD_COMMAND
    ${CMAKE_HOST${lang}_COMPILER}
    -MM
    ${BUILD_SOURCE}
    ${BUILD_INCLUDE_DIRECTORIES}
    ${BUILD_COMPILE_OPTIONS}
  )
  execute_process(
    COMMAND ${BUILD_COMMAND}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE _result
    OUTPUT_VARIABLE _output
    ERROR_QUIET
  )

  if(_result EQUAL 0)
    string(REPLACE " \\" "" _output "${_output}")
    string(REPLACE "\n" "" _output "${_output}")
    separate_arguments(_file_dependencies NATIVE_COMMAND "${_output}")
    list(REMOVE_AT _file_dependencies 0)
  else()
    set(_file_dependencies ${BUILD_SOURCE})
  endif()

  set(${OUTPUT} ${_file_dependencies} PARENT_SCOPE)
endfunction(get_host_file_dependencies)

function(get_host_absolute_paths OUTPUT INPUT)
  unset(_result)
  foreach(_path IN LISTS INPUT)
    # Skip generator expressions
    if("${_path}" MATCHES "\\$<")
      list(APPEND _result "${_path}")
    else()
      get_filename_component(_path "${_path}" ABSOLUTE)
      list(APPEND _result "${_path}")
    endif()
  endforeach()
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(get_host_absolute_paths)

function(get_host_standard_compile_option lang OUTPUT)
  if(DEFINED CMAKE_HOST${lang}_STANDARD)
    if(NOT DEFINED CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_STANDARD_COMPILE_OPTION)
      host_logging_error("HOST${lang}_STANDARD is set to invalid value '${CMAKE_HOST${lang}_STANDARD}'")
    endif()

    if(NOT DEFINED CMAKE_HOST${lang}_EXTENSIONS OR CMAKE_HOST${lang}_EXTENSIONS)
      set(${OUTPUT} "${CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_EXTENSION_COMPILE_OPTION}" PARENT_SCOPE)
    else()
      set(${OUTPUT} "${CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_STANDARD_COMPILE_OPTION}" PARENT_SCOPE)
    endif()
  endif()
endfunction(get_host_standard_compile_option)

function(find_host_language OUTPUT SOURCES)
  # Collect source file extensions
  unset(extensions)
  foreach(source IN LISTS SOURCES)
    get_filename_component(extension ${source} LAST_EXT)
    list(APPEND extensions ${extension})
  endforeach()

  # Unable to find source file extensions
  if(NOT extensions)
    unset(${OUTPUT} PARENT_SCOPE)
    return()
  endif()

  foreach(lang IN LISTS ENABLED_HOST_LANGUAGES)
    # Remove all matching extensions
    foreach(extension IN LISTS CMAKE_HOST${lang}_SOURCE_FILE_EXTENSIONS)
      list(REMOVE_ITEM extensions ".${extension}")
    endforeach()

    # If no extensions left, the appropriate host language is found
    if(NOT extensions)
      set(${OUTPUT} ${lang} PARENT_SCOPE)
      return()
    endif()
  endforeach()

  # Unable to find the appropriate host language
  unset(${OUTPUT} PARENT_SCOPE)
endfunction(find_host_language)

function(get_host_include_flag OUTPUT)
  foreach(lang IN LISTS ENABLED_HOST_LANGUAGES)
    if(CMAKE_INCLUDE_FLAG_HOST${lang})
      set(${OUTPUT} "${CMAKE_INCLUDE_FLAG_HOST${lang}}" PARENT_SCOPE)
      return()
    endif()
  endforeach()
  set(${OUTPUT} "-I" PARENT_SCOPE)
endfunction(get_host_include_flag)

function(do_host_compile lang OUTPUT)
  set(oneValueArgs SOURCE TARGET)
  set(multiValueArgs INCLUDE_DIRECTORIES COMPILE_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Reset the appropriate host language for each source file
  find_host_language(lang "${BUILD_SOURCE}")

  # Set global compile flags
  list(PREPEND BUILD_COMPILE_OPTIONS "${CMAKE_HOST${lang}_FLAGS}")

  # Set standard compile option
  get_host_standard_compile_option(${lang} _option)
  list(PREPEND BUILD_COMPILE_OPTIONS "${_option}")

  # Set path to the output file
  if(IS_ABSOLUTE "${BUILD_SOURCE}")
    file(RELATIVE_PATH BUILD_SOURCE ${CMAKE_CURRENT_SOURCE_DIR} "${BUILD_SOURCE}")
  endif()
  # Replace special characters in the path
  set(_build_source "${BUILD_SOURCE}")
  string(REPLACE ".." "__" _build_source "${_build_source}")
  string(REGEX REPLACE "[\":*?<>| ]" "_" _build_source "${_build_source}")
  set(_absolute_output "${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_HOST_TARGET_PREFIX}${BUILD_TARGET}.dir/${_build_source}${CMAKE_HOST${lang}_OUTPUT_EXTENSION}")
  file(RELATIVE_PATH _relative_output ${CMAKE_CURRENT_BINARY_DIR} "${_absolute_output}")
  file(RELATIVE_PATH _relative_gcda_output ${CMAKE_CURRENT_BINARY_DIR} "${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_HOST_TARGET_PREFIX}${BUILD_TARGET}.dir/${_build_source}.gcda")

  # Make sure that the base directory of the object file exists
  get_filename_component(BUILD_DIRECTORY "${_absolute_output}" DIRECTORY)
  file(MAKE_DIRECTORY ${BUILD_DIRECTORY})

  # Resolve absolute path
  get_filename_component(BUILD_SOURCE ${BUILD_SOURCE} ABSOLUTE)

  # Compile source file
  set(BUILD_COMMAND
    ${CMAKE_HOST${lang}_COMPILER}
    ${BUILD_INCLUDE_DIRECTORIES}
    ${BUILD_COMPILE_OPTIONS}
    -o ${_relative_output}
    -c ${BUILD_SOURCE}
  )

  add_custom_command(
    OUTPUT ${_relative_output}
    COMMAND ${CMAKE_COMMAND} -E rm -f -- ${_relative_gcda_output}
    COMMAND ${BUILD_COMMAND}
    DEPENDS ${BUILD_DEPENDS}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Building HOST${lang} object ${_relative_output}"
    COMMAND_EXPAND_LISTS
    VERBATIM
  )

  set(${OUTPUT} ${_absolute_output} PARENT_SCOPE)
endfunction(do_host_compile)

function(do_host_link lang TARGET OUTPUT)
  set(oneValueArgs TYPE VERSION SOVERSION)
  set(multiValueArgs OBJECTS LINK_LIBRARIES LINK_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Default type is EXECUTABLE
  if(NOT BUILD_TYPE)
    set(BUILD_TYPE "EXECUTABLE")
  endif()

  # Set object files
  separate_arguments(BUILD_OBJECTS NATIVE_COMMAND "${BUILD_OBJECTS}")

  # Set libraries
  transform_host_arguments(BUILD_LINK_LIBRARIES "${BUILD_LINK_LIBRARIES}" PREPEND "${CMAKE_LINK_LIBRARY_FLAG}")

  if(BUILD_TYPE STREQUAL "SHARED")
    # Set global shared linker flags
    list(PREPEND BUILD_LINK_OPTIONS "${CMAKE_HOST_SHARED_LINKER_FLAGS}")

    # Add shared library creation flags (e.g. -shared)
    list(PREPEND BUILD_LINK_OPTIONS "${CMAKE_HOST${lang}_SHARED_LIBRARY_CREATE_FLAGS}")

    if(NOT CMAKE_HOST_SHARED_LIBRARY_PREFIX)
      set(CMAKE_HOST_SHARED_LIBRARY_PREFIX "${CMAKE_HOST${lang}_SHARED_LIBRARY_PREFIX}")
    endif()
    if(NOT CMAKE_HOST_SHARED_LIBRARY_SUFFIX)
      set(CMAKE_HOST_SHARED_LIBRARY_SUFFIX "${CMAKE_HOST${lang}_SHARED_LIBRARY_SUFFIX}")
    endif()

    # Determine output filenames based on VERSION/SOVERSION
    set(_basename "${CMAKE_HOST_SHARED_LIBRARY_PREFIX}${TARGET}${CMAKE_HOST_SHARED_LIBRARY_SUFFIX}")

    if(BUILD_VERSION)
      set(_realname "${_basename}.${BUILD_VERSION}")
    elseif(BUILD_SOVERSION)
      set(_realname "${_basename}.${BUILD_SOVERSION}")
    else()
      set(_realname "${_basename}")
    endif()

    set(_output "${CMAKE_CURRENT_BINARY_DIR}/${_realname}")

    # Add SONAME flag (prefer SOVERSION, fall back to VERSION)
    if(BUILD_SOVERSION OR BUILD_VERSION)
      if(BUILD_SOVERSION)
        set(_soname "${_basename}.${BUILD_SOVERSION}")
      else()
        set(_soname "${_basename}.${BUILD_VERSION}")
      endif()
      list(APPEND BUILD_LINK_OPTIONS "${CMAKE_HOST${lang}_SHARED_LIBRARY_SONAME_FLAG}${_soname}")
    endif()

    # Link object files
    set(BUILD_COMMAND
      ${CMAKE_HOST${lang}_COMPILER}
      -o ${_output}
      ${BUILD_OBJECTS}
      ${BUILD_LINK_LIBRARIES}
      ${BUILD_LINK_OPTIONS}
    )

    # Build symlink commands for VERSION/SOVERSION
    set(_symlink_commands)
    set(_symlink_outputs)

    if(BUILD_VERSION AND BUILD_SOVERSION)
      # libhello.so.4 -> libhello.so.1.2.3
      set(_sovername "${_basename}.${BUILD_SOVERSION}")
      list(APPEND _symlink_commands
        COMMAND ${CMAKE_COMMAND} -E create_symlink ${_realname} ${CMAKE_CURRENT_BINARY_DIR}/${_sovername}
      )
      list(APPEND _symlink_outputs ${CMAKE_CURRENT_BINARY_DIR}/${_sovername})
      # libhello.so -> libhello.so.4
      list(APPEND _symlink_commands
        COMMAND ${CMAKE_COMMAND} -E create_symlink ${_sovername} ${CMAKE_CURRENT_BINARY_DIR}/${_basename}
      )
      list(APPEND _symlink_outputs ${CMAKE_CURRENT_BINARY_DIR}/${_basename})
    elseif(BUILD_VERSION OR BUILD_SOVERSION)
      # libhello.so -> libhello.so.X
      list(APPEND _symlink_commands
        COMMAND ${CMAKE_COMMAND} -E create_symlink ${_realname} ${CMAKE_CURRENT_BINARY_DIR}/${_basename}
      )
      list(APPEND _symlink_outputs ${CMAKE_CURRENT_BINARY_DIR}/${_basename})
    endif()

    add_custom_command(
      OUTPUT ${_output} ${_symlink_outputs}
      COMMAND ${BUILD_COMMAND}
      ${_symlink_commands}
      DEPENDS ${BUILD_OBJECTS} ${BUILD_DEPENDS}
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
      COMMENT "Linking HOST${lang} shared library ${_realname}"
      COMMAND_EXPAND_LISTS
      VERBATIM
    )
  else()
    # EXECUTABLE (existing behavior)
    # Set global linker flags
    list(PREPEND BUILD_LINK_OPTIONS "${CMAKE_HOST_EXE_LINKER_FLAGS}")

    if(NOT CMAKE_HOST_EXECUTABLE_SUFFIX)
      set(CMAKE_HOST_EXECUTABLE_SUFFIX "${CMAKE_HOST${lang}_EXECUTABLE_SUFFIX}")
    endif()

    set(_filename "${TARGET}${CMAKE_HOST_EXECUTABLE_SUFFIX}")
    set(_output "${CMAKE_CURRENT_BINARY_DIR}/${_filename}")

    # Link object files
    set(BUILD_COMMAND
      ${CMAKE_HOST${lang}_COMPILER}
      -o ${_output}
      ${BUILD_OBJECTS}
      ${BUILD_LINK_LIBRARIES}
      ${BUILD_LINK_OPTIONS}
    )

    add_custom_command(
      OUTPUT ${_output}
      COMMAND ${BUILD_COMMAND}
      DEPENDS ${BUILD_OBJECTS} ${BUILD_DEPENDS}
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
      COMMENT "Linking HOST${lang} executable ${_filename}"
      COMMAND_EXPAND_LISTS
      VERBATIM
    )
  endif()

  set(${OUTPUT} ${_output} PARENT_SCOPE)
endfunction(do_host_link)

function(add_host_executable TARGET)
  set(options EXCLUDE_FROM_ALL)
  set(multiValueArgs SOURCES INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS LINK_LIBRARIES DEPENDS)
  cmake_parse_arguments(BUILD "${options}" "" "${multiValueArgs}" ${ARGN})

  # Remove host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Set include directories
  get_host_include_flag(include_flag)
  separate_host_scoped_arguments("${BUILD_INCLUDE_DIRECTORIES}" BUILD_INCLUDE_DIRECTORIES BUILD_INTERFACE_INCLUDE_DIRECTORIES)
  get_host_absolute_paths(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}")
  transform_host_arguments(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}" PREPEND "${include_flag}")

  # Set global include directories
  unset(_global_include_directories)
  transform_host_arguments(_global_include_directories "${CMAKE_HOST_INCLUDE_PATH}" PREPEND "${include_flag}")

  # Set compile options
  separate_host_scoped_arguments("${BUILD_COMPILE_OPTIONS}" BUILD_COMPILE_OPTIONS BUILD_INTERFACE_COMPILE_OPTIONS)

  # Set link options
  separate_host_scoped_arguments("${BUILD_LINK_OPTIONS}" BUILD_LINK_OPTIONS BUILD_INTERFACE_LINK_OPTIONS)

  # Set link libraries
  separate_host_scoped_arguments("${BUILD_LINK_LIBRARIES}" BUILD_LINK_LIBRARIES BUILD_INTERFACE_LINK_LIBRARIES)
  get_host_target_names(BUILD_LINK_LIBRARIES "${BUILD_LINK_LIBRARIES}")

  # Ensure only host libraries are given
  set(remaining ${BUILD_LINK_LIBRARIES})
  list(FILTER remaining EXCLUDE REGEX "^${CMAKE_HOST_TARGET_PREFIX}.*$")
  list(JOIN remaining ", " remaining)
  if(remaining)
    host_logging_error("add_host_executable LINK_LIBRARIES requires the name of host libraries starting with the host namespace prefix.\nUnsupported libraries: ${remaining}")
  endif()

  # Get interface properties of linking libraries
  unset(_extra_include_directories)
  unset(_extra_compile_options)
  unset(_extra_link_options)
  unset(_extra_dependencies)

  foreach(_lib IN LISTS BUILD_LINK_LIBRARIES)
    list(APPEND _extra_include_directories "$<$<BOOL:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_INCLUDE_DIRECTORIES>>:${include_flag}>$<JOIN:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_INCLUDE_DIRECTORIES>,$<SEMICOLON>${include_flag}>")
    list(APPEND _extra_compile_options "$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_COMPILE_OPTIONS>")
    list(APPEND _extra_link_options "$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_LINK_OPTIONS>")
    list(APPEND _extra_dependencies "${CMAKE_HOST_TARGET_PREFIX}$<TARGET_PROPERTY:${_lib},HOST_NAME>")
    # Add static library paths as link option
    # Note: $<TARGET_PROPERTY:tgt,prop>: Non-existing libraries cause build failures
    list(APPEND _extra_link_options "$<$<BOOL:$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_STATIC>>:$<TARGET_PROPERTY:${_lib},HOST_OUTPUT_NAME>>")
    # Add shared library link flags: -L<dir> -l<name>
    list(APPEND _extra_link_options "$<$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_SHARED>:-L${CMAKE_CURRENT_BINARY_DIR}>")
    list(APPEND _extra_link_options "$<$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_SHARED>:-l$<TARGET_PROPERTY:${_lib},HOST_NAME>>")
  endforeach()

  if(NOT BUILD_SOURCES)
    host_logging_error("No SOURCES given to target: ${TARGET}")
  endif()

  find_host_language(lang "${BUILD_SOURCES}")
  if(NOT lang)
    host_logging_error("CMake Error: Cannot determine host language for target: ${TARGET}")
  endif()

  # Compile source files
  unset(_objects)

  foreach(_source IN LISTS BUILD_SOURCES)
    # Check if the source file exists
    if(IS_ABSOLUTE "${_source}")
      set(_path "${_source}")
    else()
      set(_path "${CMAKE_CURRENT_SOURCE_DIR}/${_source}")
    endif()
    if(NOT EXISTS "${_path}")
      host_logging_error("Cannot find source file:\n  ${_source}")
    endif()

    # Resolve file dependencies
    get_host_file_dependencies(${lang} _file_dependencies
      SOURCE "${_source}"
      INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
      COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}"
    )

    do_host_compile(${lang} _output
      SOURCE "${_source}"
      TARGET "${TARGET}"
      INCLUDE_DIRECTORIES "${_global_include_directories}" "${BUILD_INCLUDE_DIRECTORIES}" "${_extra_include_directories}"
      COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" "${_extra_compile_options}"
      DEPENDS "${BUILD_DEPENDS}" "${_file_dependencies}" "${_extra_dependencies}"
    )
    list(APPEND _objects ${_output})
  endforeach()

  # Add RPATH for shared library dependencies
  if(NOT CMAKE_HOST_SKIP_BUILD_RPATH)
    foreach(_lib IN LISTS BUILD_LINK_LIBRARIES)
      list(APPEND _extra_link_options "$<$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_SHARED>:${CMAKE_HOST${lang}_SHARED_LIBRARY_RUNTIME_FLAG}${CMAKE_CURRENT_BINARY_DIR}>")
    endforeach()
  endif()

  # Add user-specified RPATH
  if(CMAKE_HOST_BUILD_RPATH)
    list(APPEND _extra_link_options "${CMAKE_HOST${lang}_SHARED_LIBRARY_RUNTIME_FLAG}${CMAKE_HOST_BUILD_RPATH}")
  endif()

  # Link object files
  do_host_link(${lang} ${TARGET} _output
    OBJECTS "${_objects}"
    LINK_OPTIONS "${BUILD_LINK_OPTIONS}" "${_extra_link_options}"
    DEPENDS "${BUILD_DEPENDS}" "${_extra_dependencies}"
  )

  add_host_custom_target("${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}" DEPENDS "${_output}")

  if(NOT BUILD_EXCLUDE_FROM_ALL)
    add_host_dependencies("${CMAKE_HOST_BUILD_TARGET}" "${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}")
  endif()

  set_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    NAME "${TARGET}"
    OUTPUT_NAME "${_output}"
    TYPE "HOST_EXECUTABLE"
    SOURCES "${BUILD_SOURCES}"
  )
endfunction(add_host_executable)

function(add_host_library TARGET TYPE)
  set(options EXCLUDE_FROM_ALL)
  set(oneValueArgs VERSION SOVERSION)
  set(multiValueArgs SOURCES INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS LINK_LIBRARIES DEPENDS)
  cmake_parse_arguments(BUILD "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Remove host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Set include directories
  get_host_include_flag(include_flag)
  separate_host_scoped_arguments("${BUILD_INCLUDE_DIRECTORIES}" BUILD_INCLUDE_DIRECTORIES BUILD_INTERFACE_INCLUDE_DIRECTORIES)
  get_host_absolute_paths(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}")
  transform_host_arguments(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}" PREPEND "${include_flag}")
  get_host_absolute_paths(BUILD_INTERFACE_INCLUDE_DIRECTORIES "${BUILD_INTERFACE_INCLUDE_DIRECTORIES}")

  # Set global include directories
  unset(_global_include_directories)
  transform_host_arguments(_global_include_directories "${CMAKE_HOST_INCLUDE_PATH}" PREPEND "${include_flag}")

  # Set compile options
  separate_host_scoped_arguments("${BUILD_COMPILE_OPTIONS}" BUILD_COMPILE_OPTIONS BUILD_INTERFACE_COMPILE_OPTIONS)

  # Set link options
  separate_host_scoped_arguments("${BUILD_LINK_OPTIONS}" BUILD_LINK_OPTIONS BUILD_INTERFACE_LINK_OPTIONS)

  # Set link libraries
  separate_host_scoped_arguments("${BUILD_LINK_LIBRARIES}" BUILD_LINK_LIBRARIES BUILD_INTERFACE_LINK_LIBRARIES)
  get_host_target_names(BUILD_LINK_LIBRARIES "${BUILD_LINK_LIBRARIES}")

  # Get interface properties of linking libraries
  unset(_extra_include_directories)
  unset(_extra_compile_options)
  unset(_extra_link_options)
  unset(_extra_dependencies)

  # Ensure only host libraries are given
  set(remaining ${BUILD_LINK_LIBRARIES})
  list(FILTER remaining EXCLUDE REGEX "^${CMAKE_HOST_TARGET_PREFIX}.*$")
  list(JOIN remaining ", " remaining)
  if(remaining)
    host_logging_error("add_host_library LINK_LIBRARIES requires the name of host libraries starting with the host namespace prefix.\nUnsupported libraries: ${remaining}")
  endif()

  foreach(_lib IN LISTS BUILD_LINK_LIBRARIES)
    list(APPEND _extra_include_directories "$<$<BOOL:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_INCLUDE_DIRECTORIES>>:${include_flag}>$<JOIN:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_INCLUDE_DIRECTORIES>,$<SEMICOLON>${include_flag}>")
    list(APPEND _extra_compile_options "$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_COMPILE_OPTIONS>")
    list(APPEND _extra_link_options "$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_LINK_OPTIONS>")
    list(APPEND _extra_dependencies "${CMAKE_HOST_TARGET_PREFIX}$<TARGET_PROPERTY:${_lib},HOST_NAME>")
    # Add static library paths as link option
    list(APPEND _extra_link_options "$<$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_STATIC>:$<TARGET_PROPERTY:${_lib},HOST_OUTPUT_NAME>>")
    # Add shared library link flags: -L<dir> -l<name>
    list(APPEND _extra_link_options "$<$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_SHARED>:-L${CMAKE_CURRENT_BINARY_DIR}>")
    list(APPEND _extra_link_options "$<$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_SHARED>:-l$<TARGET_PROPERTY:${_lib},HOST_NAME>>")
  endforeach()

  set(BUILD_TYPE "HOST_${TYPE}")

  if(BUILD_TYPE STREQUAL "HOST_STATIC")
    if(NOT BUILD_SOURCES)
      host_logging_error("No SOURCES given to target: ${TARGET}")
    endif()

    find_host_language(lang "${BUILD_SOURCES}")
    if(NOT lang)
      host_logging_error("CMake Error: Cannot determine host language for target: ${TARGET}")
    endif()

    if(NOT CMAKE_HOST_STATIC_LIBRARY_PREFIX)
      set(CMAKE_HOST_STATIC_LIBRARY_PREFIX "${CMAKE_HOST${lang}_STATIC_LIBRARY_PREFIX}")
    endif()
    if(NOT CMAKE_HOST_STATIC_LIBRARY_SUFFIX)
      set(CMAKE_HOST_STATIC_LIBRARY_SUFFIX "${CMAKE_HOST${lang}_STATIC_LIBRARY_SUFFIX}")
    endif()

    # Compile source files
    unset(_objects)

    foreach(_source IN LISTS BUILD_SOURCES)
      # Check if the source file exists
      if(IS_ABSOLUTE "${_source}")
        set(_path "${_source}")
      else()
        set(_path "${CMAKE_CURRENT_SOURCE_DIR}/${_source}")
      endif()
      if(NOT EXISTS "${_path}")
        host_logging_error("Cannot find source file:\n  ${_source}")
      endif()

      # Resolve file dependencies
      get_host_file_dependencies(${lang} _file_dependencies
        SOURCE "${_source}"
        INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}"
      )

      do_host_compile(${lang} _output
        SOURCE "${_source}"
        TARGET "${CMAKE_HOST_STATIC_LIBRARY_PREFIX}${TARGET}${CMAKE_HOST_STATIC_LIBRARY_SUFFIX}"
        INCLUDE_DIRECTORIES "${_global_include_directories}" "${BUILD_INCLUDE_DIRECTORIES}" "${_extra_include_directories}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" "${_extra_compile_options}"
        DEPENDS "${BUILD_DEPENDS}" "${_file_dependencies}" "${_extra_dependencies}"
      )
      list(APPEND _objects ${_output})
    endforeach()

    set(_filename "${CMAKE_HOST_STATIC_LIBRARY_PREFIX}${TARGET}${CMAKE_HOST_STATIC_LIBRARY_SUFFIX}")
    set(_output "${CMAKE_CURRENT_BINARY_DIR}/${_filename}")
    set(_response_file "${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_HOST_TARGET_PREFIX}${_filename}.dir/${_filename}.rsp")

    file(GENERATE
      OUTPUT ${_response_file}
      CONTENT "$<JOIN:${_objects},\n>"
    )

    if(NOT CMAKE_HOST_AR)
      set(CMAKE_HOST_AR "${CMAKE_HOST${lang}_AR}")
    endif()
    if(NOT CMAKE_HOST_RANLIB)
      set(CMAKE_HOST_RANLIB "${CMAKE_HOST${lang}_RANLIB}")
    endif()

    # Archive object files to create a static library
    add_custom_command(
      OUTPUT ${_output}
      COMMAND ${CMAKE_HOST_AR} rc ${_output} @${_response_file}
      COMMAND ${CMAKE_HOST_RANLIB} ${_output}
      DEPENDS ${_objects} ${BUILD_DEPENDS}
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
      COMMENT "Linking HOST${lang} static library ${_filename}"
      COMMAND_EXPAND_LISTS
      VERBATIM
    )
    add_host_custom_target("${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}" DEPENDS "${_output}")
  elseif(BUILD_TYPE STREQUAL "HOST_SHARED")
    if(NOT BUILD_SOURCES)
      host_logging_error("No SOURCES given to target: ${TARGET}")
    endif()

    find_host_language(lang "${BUILD_SOURCES}")
    if(NOT lang)
      host_logging_error("CMake Error: Cannot determine host language for target: ${TARGET}")
    endif()

    # Add PIC compile option for shared libraries
    if(NOT DEFINED CMAKE_HOST_POSITION_INDEPENDENT_CODE OR CMAKE_HOST_POSITION_INDEPENDENT_CODE)
      list(PREPEND BUILD_COMPILE_OPTIONS "${CMAKE_HOST${lang}_COMPILE_OPTIONS_PIC}")
    endif()

    if(NOT CMAKE_HOST_SHARED_LIBRARY_PREFIX)
      set(CMAKE_HOST_SHARED_LIBRARY_PREFIX "${CMAKE_HOST${lang}_SHARED_LIBRARY_PREFIX}")
    endif()
    if(NOT CMAKE_HOST_SHARED_LIBRARY_SUFFIX)
      set(CMAKE_HOST_SHARED_LIBRARY_SUFFIX "${CMAKE_HOST${lang}_SHARED_LIBRARY_SUFFIX}")
    endif()

    # Compile source files
    unset(_objects)

    foreach(_source IN LISTS BUILD_SOURCES)
      # Check if the source file exists
      if(IS_ABSOLUTE "${_source}")
        set(_path "${_source}")
      else()
        set(_path "${CMAKE_CURRENT_SOURCE_DIR}/${_source}")
      endif()
      if(NOT EXISTS "${_path}")
        host_logging_error("Cannot find source file:\n  ${_source}")
      endif()

      # Resolve file dependencies
      get_host_file_dependencies(${lang} _file_dependencies
        SOURCE "${_source}"
        INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}"
      )

      do_host_compile(${lang} _output
        SOURCE "${_source}"
        TARGET "${CMAKE_HOST_SHARED_LIBRARY_PREFIX}${TARGET}${CMAKE_HOST_SHARED_LIBRARY_SUFFIX}"
        INCLUDE_DIRECTORIES "${_global_include_directories}" "${BUILD_INCLUDE_DIRECTORIES}" "${_extra_include_directories}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" "${_extra_compile_options}"
        DEPENDS "${BUILD_DEPENDS}" "${_file_dependencies}" "${_extra_dependencies}"
      )
      list(APPEND _objects ${_output})
    endforeach()

    # Link shared library
    do_host_link(${lang} ${TARGET} _output
      TYPE SHARED
      VERSION "${BUILD_VERSION}"
      SOVERSION "${BUILD_SOVERSION}"
      OBJECTS "${_objects}"
      LINK_OPTIONS "${BUILD_LINK_OPTIONS}" "${_extra_link_options}"
      DEPENDS "${BUILD_DEPENDS}" "${_extra_dependencies}"
    )
    add_host_custom_target("${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}" DEPENDS "${_output}")
  elseif(BUILD_TYPE STREQUAL "HOST_INTERFACE")
    if(BUILD_SOURCES)
      host_logging_error("add_host_library INTERFACE requires no source arguments.")
    endif()
    # Create a phony target for an interface library
    add_host_custom_target("${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}")
  else()
    host_logging_error("Unsupported library type: ${TYPE}")
  endif()

  if(NOT BUILD_EXCLUDE_FROM_ALL)
    add_host_dependencies("${CMAKE_HOST_BUILD_TARGET}" "${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}")
  endif()

  set_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    NAME "${TARGET}"
    OUTPUT_NAME "${_output}"
    TYPE "${BUILD_TYPE}"
    SOURCES "${BUILD_SOURCES}"
    INTERFACE_INCLUDE_DIRECTORIES "${BUILD_INTERFACE_INCLUDE_DIRECTORIES}"
    INTERFACE_COMPILE_OPTIONS "${BUILD_INTERFACE_COMPILE_OPTIONS}"
    INTERFACE_LINK_OPTIONS "${BUILD_INTERFACE_LINK_OPTIONS}"
    VERSION "${BUILD_VERSION}"
    SOVERSION "${BUILD_SOVERSION}"
  )
endfunction(add_host_library)
