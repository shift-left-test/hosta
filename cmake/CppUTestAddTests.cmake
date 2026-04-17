# Copyright (c) 2026 LG Electronics Inc.
# SPDX-License-Identifier: MIT

set(prefix "${TEST_PREFIX}")
set(extra_args ${TEST_EXTRA_ARGS})
set(properties ${TEST_PROPERTIES})
set(script)
set(suite)
set(tests)

function(add_command NAME)
  set(_args "")
  foreach(_arg ${ARGN})
    set(_args "${_args} ${_arg}")
  endforeach()
  set(script "${script}${NAME}(${_args})\n" PARENT_SCOPE)
endfunction()

# Check if the test executable exists
if(NOT EXISTS "${TEST_EXECUTABLE}")
  message(FATAL_ERROR
    "Specified test executable does not exist.\n"
    "  Path: '${TEST_EXECUTABLE}'"
  )
endif()

# Run test executable with -ln to get list of available tests without executing them
# CppUTest -ln outputs: Group1.Name1 Group2.Name2 ... (space-separated, single line)
execute_process(
  COMMAND "${TEST_EXECUTABLE}" -ln
  WORKING_DIRECTORY "${TEST_WORKING_DIRECTORY}"
  TIMEOUT ${TEST_DISCOVERY_TIMEOUT}
  OUTPUT_VARIABLE output
  RESULT_VARIABLE result
)
if(NOT ${result} EQUAL 0)
  string(REPLACE "\n" "\n    " output "${output}")
  message(FATAL_ERROR
    "Error running test executable.\n"
    "  Path: '${TEST_EXECUTABLE}'\n"
    "  Result: ${result}\n"
    "  Output:\n"
    "    ${output}\n"
  )
endif()

# Parse space-separated Group.Name pairs
string(STRIP "${output}" output)
separate_arguments(test_list NATIVE_COMMAND "${output}")

foreach(test_entry ${test_list})
  # Split Group.Name into group and name
  string(REGEX MATCH "^([A-Za-z_0-9]+)\\.([A-Za-z_0-9]+)$" matched "${test_entry}")
  if(NOT matched)
    continue()
  endif()
  set(cpputest_test_group "${CMAKE_MATCH_1}")
  set(cpputest_test_case "${CMAKE_MATCH_2}")
  set(cpputest_test_name "${cpputest_test_group}.${cpputest_test_case}")

  set(ctest_test_name ${prefix}${cpputest_test_name})
  add_command(add_test
    "${ctest_test_name}"
    "${TEST_EXECUTABLE}"
    -sg "${cpputest_test_group}"
    -sn "${cpputest_test_case}"
    ${extra_args}
  )
  add_command(set_tests_properties
    ${ctest_test_name}
    PROPERTIES
    WORKING_DIRECTORY "${TEST_WORKING_DIRECTORY}"
    ${properties}
  )
  list(APPEND tests "${ctest_test_name}")
endforeach()

# Create a list of all discovered tests
add_command(set ${TEST_LIST} ${tests})

# Write CTest script
file(WRITE "${CTEST_FILE}" "${script}")
