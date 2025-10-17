# Copyright (c) 2025 LG Electronics Inc.
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

# Check if the test executbale exists
if(NOT EXISTS "${TEST_EXECUTABLE}")
  message(FATAL_ERROR
    "Specified test executable does not exist.\n"
    "  Path: '${TEST_EXECUTABLE}'"
  )
endif()

# Check if the test executable supports dry-run mode
execute_process(
  COMMAND "${TEST_EXECUTABLE}" -h
  WORKING_DIRECTORY "${TEST_WORKING_DIRECTORY}"
  TIMEOUT ${TEST_DISCOVERY_TIMEOUT}
  OUTPUT_VARIABLE output
  RESULT_VARIABLE result
)
if(NOT output MATCHES "Unity")
  message(FATAL_ERROR
    "Error running test executable.\n"
    "  Path: '${TEST_EXECUTABLE}'\n"
    "  Result: ${result}\n"
  )
endif()
if(NOT output MATCHES "-d          Dry run all tests")
  message(FATAL_ERROR
    "Missing dry-run option. Upgrade Unity Fixture to the latest version.\n"
    "  Path: '${TEST_EXECUTABLE}'\n"
    "  Result: ${result}\n"
  )
endif()

# Run test executable to get list of available tests
execute_process(
  COMMAND "${TEST_EXECUTABLE}" -d -v
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

# Add tests with CTest by scanning console output
set(unity_test_name_regex ".*\\([ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*,[ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*\\).*")
set(unity_test_type_regex "([^A-Za-z_0-9](IGNORE_)?TEST)")

string(REGEX MATCHALL "${unity_test_type_regex}[ \r\n\t]*\\(([A-Za-z_0-9 ,\r\n\t]+)\\)" found_tests "${output}")

foreach(hit ${found_tests})
  string(STRIP ${hit} hit)
  string(REGEX REPLACE ${unity_test_name_regex} "\\1.\\2" unity_test_name ${hit})
  string(REGEX REPLACE ${unity_test_name_regex} "\\1" unity_test_group ${hit})
  string(REGEX REPLACE ${unity_test_name_regex} "\\2" unity_test_case ${hit})

  # Add test
  set(ctest_test_name ${prefix}${unity_test_name})
  add_command(add_test
    "${ctest_test_name}"
    "${TEST_EXECUTABLE}"
    -G "${unity_test_group}"
    -N "${unity_test_case}"
    -v
    ${extra_args}
  )

  # Make sure ignored unity tests get disabled in CTest
  if(hit MATCHES "(^|\\.)IGNORE_")
    add_command(set_tests_properties
      ${ctest_test_name}
      PROPERTIES DISABLED TRUE
    )
  endif()
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
