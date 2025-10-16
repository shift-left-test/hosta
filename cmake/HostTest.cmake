# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

# Set the directory of the current file
if(NOT _HOSTA_BASE_DIR)
  set(_HOSTA_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")
endif()

include(CMakeParseArguments)
include(${_HOSTA_BASE_DIR}/HostBuild.cmake)

function(add_host_test TARGET)
  # Assume that enable_testing() is called
  if(NOT CMAKE_TESTING_ENABLED)
    return()
  endif()

  set(oneValueArgs PREFIX)
  set(multiValueArgs EXTRA_ARGS)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Remove the host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Path to the executable
  get_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    OUTPUT_NAME _output
  )

  add_test(NAME ${ARG_PREFIX}${TARGET} COMMAND ${_output} ${ARG_EXTRA_ARGS})
endfunction(add_host_test)

function(unity_fixture_add_host_tests TARGET)
  # Assume that enable_testing() is called
  if(NOT CMAKE_TESTING_ENABLED)
    return()
  endif()

  set(oneValueArgs PREFIX)
  set(multiValueArgs EXTRA_ARGS)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Remove the host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Path to the executable and source files
  get_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    SOURCES _sources
    SOURCE_DIR _source_dir
    OUTPUT_NAME _output
  )

  # Convert relative source paths to absolute ones
  unset(sources)
  foreach(source IN LISTS _sources)
    if(IS_ABSOLUTE "${source}")
      list(APPEND sources "${source}")
    else()
      list(APPEND sources "${_source_dir}/${source}")
    endif()
  endforeach()

  # Add tests with CTest by scanning source code for Unity test macros
  set(unity_test_name_regex ".*\\([ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*,[ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*\\).*")
  set(unity_test_ignored_regex "([^A-Za-z_0-9]IGNORE_TEST)")
  set(unity_test_type_regex "([^A-Za-z_0-9]RUN_TEST_CASE)")

  # Find the list of ignored tests
  set(ignored_tests)
  foreach(source IN LISTS sources)
    file(READ "${source}" contents)

    # Remove comments
    string(REGEX REPLACE "//[^\r\n]*" "" contents "${contents}")
    string(REGEX REPLACE "/\\*([^*]|\\*+[^*/])*\\*/" "" contents "${contents}")

    string(REGEX MATCHALL "${unity_test_ignored_regex}[ \r\n\t]*\\(([A-Za-z_0-9 ,\r\n\t]+)\\)" found_tests "${contents}")
    foreach(hit ${found_tests})
      string(STRIP ${hit} hit)
      string(REGEX REPLACE ${unity_test_name_regex} "\\1.\\2" unity_test_name ${hit})
      list(APPEND ignored_tests ${unity_test_name})
    endforeach()
  endforeach()

  # Find the list of runnable tests
  set(added_tests)
  foreach(source IN LISTS sources)
    file(READ "${source}" contents)

    # Remove comments
    string(REGEX REPLACE "//[^\r\n]*" "" contents "${contents}")
    string(REGEX REPLACE "/\\*([^*]|\\*+[^*/])*\\*/" "" contents "${contents}")

    string(REGEX MATCHALL "${unity_test_type_regex}[ \r\n\t]*\\(([A-Za-z_0-9 ,\r\n\t]+)\\)" found_tests "${contents}")
    foreach(hit ${found_tests})
      string(STRIP ${hit} hit)
      string(REGEX REPLACE ${unity_test_name_regex} "\\1.\\2" unity_test_name ${hit})
      string(REGEX REPLACE ${unity_test_name_regex} "\\1" unity_test_group ${hit})
      string(REGEX REPLACE ${unity_test_name_regex} "\\2" unity_test_case ${hit})

      # Ignore already added tests
      if(unity_test_name IN_LIST added_tests)
        continue()
      endif()

      set(ctest_test_name ${ARG_PREFIX}${unity_test_name})
      if(ENABLE_HOST_UNITY_FIXTURE_EXACT_MATCH)
        add_test(NAME ${ctest_test_name} COMMAND ${_output} -G ${unity_test_group} -N ${unity_test_case} -v ${ARG_EXTRA_ARGS})
      else()
        add_test(NAME ${ctest_test_name} COMMAND ${_output} -g ${unity_test_group} -n ${unity_test_case} -v ${ARG_EXTRA_ARGS})
      endif()
      list(APPEND added_tests ${unity_test_name})

      # Make sure ignored unity tests get disabled in CTest
      if(unity_test_name IN_LIST ignored_tests)
        set_tests_properties(${ctest_test_name} PROPERTIES DISABLED TRUE)  # Intended test execution
      else()
        set_tests_properties(${ctest_test_name} PROPERTIES SKIP_REGULAR_EXPRESSION "0 Tests|^$")  # Unintended test execution
      endif()
    endforeach()
  endforeach()
endfunction(unity_fixture_add_host_tests)

set(UNITY_FIXTURE_DISCOVER_HOST_TESTS_SCRIPT
  ${CMAKE_CURRENT_LIST_DIR}/UnityFixtureAddTests.cmake
)

function(unity_fixture_discover_host_tests TARGET)
  # Assume that enable_testing() is called
  if(NOT CMAKE_TESTING_ENABLED)
    return()
  endif()

  # Remove the host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Path to the executable
  get_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    OUTPUT_NAME _output
  )

  set(oneValueArgs PREFIX WORKING_DIRECTORY TEST_LIST DISCOVERY_TIMEOUT)
  set(multiValueArgs EXTRA_ARGS PROPERTIES)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  if(NOT ARG_WORKING_DIRECTORY)
    set(ARG_WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}")
  endif()
  if(NOT ARG_TEST_LIST)
    set(ARG_TEST_LIST ${TARGET}_TESTS)
  endif()
  if(NOT ARG_DISCOVERY_TIMEOUT)
    set(ARG_DISCOVERY_TIMEOUT 5)
  endif()

  get_property(
    has_counter
    TARGET "${CMAKE_HOST_TARGET_PREFIX}${TARGET}"
    PROPERTY CTEST_DISCOVERED_TEST_COUNTER
    SET
  )
  if(has_counter)
    get_property(
      counter
      TARGET "${CMAKE_HOST_TARGET_PREFIX}${TARGET}"
      PROPERTY CTEST_DISCOVERED_TEST_COUNTER
    )
    math(EXPR counter "${counter} + 1")
  else()
    set(counter 1)
  endif()
  set_property(
    TARGET "${CMAKE_HOST_TARGET_PREFIX}${TARGET}"
    PROPERTY CTEST_DISCOVERED_TEST_COUNTER
    ${counter}
  )

  set(ctest_file_base "${CMAKE_CURRENT_BINARY_DIR}/${TARGET}[${counter}]")
  set(ctest_include_file "${ctest_file_base}_include.cmake")
  set(ctest_tests_file "${ctest_file_base}_tests.cmake")
  add_custom_command(
    TARGET "${CMAKE_HOST_TARGET_PREFIX}${TARGET}" POST_BUILD
    BYPRODUCTS "${ctest_tests_file}"
    COMMAND "${CMAKE_COMMAND}"
            -D "TEST_TARGET=${CMAKE_HOST_TARGET_PREFIX}${TARGET}"
            -D "TEST_EXECUTABLE=${_output}"
            -D "TEST_WORKING_DIRECTORY=${ARG_WORKING_DIRECTORY}"
            -D "TEST_EXTRA_ARGS=${ARG_EXTRA_ARGS}"
            -D "TEST_PROPERTIES=${ARG_PROPERTIES}"
            -D "TEST_PREFIX=${ARG_PREFIX}"
            -D "TEST_LIST=${ARG_TEST_LIST}"
            -D "CTEST_FILE=${ctest_tests_file}"
            -D "TEST_DISCOVERY_TIMEOUT=${ARG_DISCOVERY_TIMEOUT}"
            -P "${UNITY_FIXTURE_DISCOVER_HOST_TESTS_SCRIPT}"
    VERBATIM
  )
  file(WRITE "${ctest_include_file}"
    "if(EXISTS \"${ctest_tests_file}\")\n"
    "  include(\"${ctest_tests_file}\")\n"
    "else()\n"
    "  add_test(${TARGET}_NOT_BUILT ${TARGET}_NOT_BUILT)\n"
    "endif()\n"
  )

  # Add discovered tests to directory TEST_INCLUDE_FILES
  set_property(DIRECTORY
    APPEND PROPERTY TEST_INCLUDE_FILES "${ctest_include_file}"
  )
endfunction(unity_fixture_discover_host_tests)

function(gtest_add_host_tests TARGET)
  # Assume that enable_testing() is called
  if(NOT CMAKE_TESTING_ENABLED)
    return()
  endif()

  set(multiValueArgs EXTRA_ARGS)
  set(oneValueArgs PREFIX)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Remove the host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Path to the executable and source files
  get_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    SOURCES _sources
    SOURCE_DIR _source_dir
    OUTPUT_NAME _output
  )

  # Convert relative source paths to absolute ones
  unset(sources)
  foreach(source IN LISTS _sources)
    if(IS_ABSOLUTE "${source}")
      list(APPEND sources "${source}")
    else()
      list(APPEND sources "${_source_dir}/${source}")
    endif()
  endforeach()

  # Use gtest_add_tests
  include(GoogleTest)
  # Set TEST_PREFIX conditionally to avoid warnings on CMake 3.31.0 or later
  if(ARG_PREFIX)
    gtest_add_tests(
      TARGET ${TARGET}
      SOURCES ${sources}
      EXTRA_ARGS ${ARG_EXTRA_ARGS}
      TEST_PREFIX ${ARG_PREFIX}
    )
  else()
    gtest_add_tests(
      TARGET ${TARGET}
      SOURCES ${sources}
      EXTRA_ARGS ${ARG_EXTRA_ARGS}
    )
  endif()
endfunction(gtest_add_host_tests)
