# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

# Set the directory of the current file
if(NOT _HOSTA_BASE_DIR)
  set(_HOSTA_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")
endif()

# The compiler configuration was forced by the user.
# Assume the user has configured all compiler information
if(CMAKE_HOSTC_COMPILER_FORCED)
  set(CMAKE_HOSTC_COMPILER_WORKS TRUE)
  list(APPEND ENABLED_HOST_LANGUAGES C)
  return()
endif()

include(${_HOSTA_BASE_DIR}/HostCompilerUtilities.cmake)

# Load host compiler preferences
load_host_compiler_preferences(C)

# Assume that the host compiler works properly
if(CMAKE_HOSTC_COMPILER_WORKS)
  if(NOT EXISTS "${CMAKE_HOSTC_COMPILER}")
    message(WARNING "Cached HOSTC compiler '${CMAKE_HOSTC_COMPILER}' no longer exists. Re-detecting...")
  else()
    list(APPEND ENABLED_HOST_LANGUAGES C)
    return()
  endif()
endif()

include(CMakeTestCompilerCommon)

# List compilers to try
if(NOT CMAKE_HOSTC_COMPILER_LIST)
  set(CMAKE_HOSTC_COMPILER_LIST cc gcc clang)
endif()

find_host_compiler(C)

# Check if a host compiler is available
if(NOT CMAKE_HOSTC_COMPILER)
  host_logging_error(
    "The CMAKE_HOSTC_COMPILER:"
    "  ${CMAKE_HOSTC_COMPILER_LIST}\n"
    "is not a full path and was not found in the PATH."
  )
endif()

# Build a small source file to identify the compiler.
find_host_compiler_id(C FLAGS "-D__CLASSIC_C__")

# Test if the host compiler can compile the most basic of programs.
# If not, a fatal error is set and stops processing commands.
PrintTestCompilerStatus("HOSTC" "")

file(WRITE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/testHOSTCCompiler.c
  "#ifdef __cplusplus\n"
  "# error \"The CMAKE_HOSTC_COMPILER is set to a C++ compiler\"\n"
  "#endif\n"
  "#if defined(__CLASSIC_C__)\n"
  "int main(argc, argv)\n"
  "  int argc;\n"
  "  char* argv[];\n"
  "#else\n"
  "int main(int argc, char* argv[])\n"
  "#endif\n"
  "{ (void)argv; return argc-1;}\n"
)

try_host_compile(C
  SOURCE testHOSTCCompiler.c
  TARGET testHOSTCCompiler.bin
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp
  RESULT_VARIABLE CMAKE_HOSTC_COMPILER_WORKS
  OUTPUT_VARIABLE __CMAKE_HOSTC_COMPILER_WORKS_OUTPUT
)

if(NOT CMAKE_HOSTC_COMPILER_WORKS)
  PrintTestCompilerStatus("HOSTC" " -- broken")

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log
    "Determining if the HOSTC compiler works failed with "
    "the following output:\n${__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT}\n\n"
  )
  string(REPLACE "\n" "\n  " _output "${__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT}")
  message(FATAL_ERROR "The HOSTC compiler\n  \"${CMAKE_HOSTC_COMPILER}\"\n"
    "is not able to compile a simple test program.\nIt fails "
    "with the following output:\n  ${_output}\n\n"
    "CMake will not be able to correctly generate this project."
  )
else()
  PrintTestCompilerStatus("HOSTC" " -- works")

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Determining if the HOSTC compiler works passed with "
    "the following output:\n${__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT}\n\n"
  )

  # Try to identify the ABI
  try_host_compile(C
    SOURCE ${CMAKE_ROOT}/Modules/CMakeCCompilerABI.c
    TARGET CMakeDetermineCompilerABI_HOSTC.bin
    COMPILE_OPTIONS ${CMAKE_HOSTC_VERBOSE_FLAG}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION}-hosta.internal
    RESULT_VARIABLE CMAKE_HOSTC_ABI_COMPILED
    OUTPUT_VARIABLE __CMAKE_HOSTC_ABI_COMPILED_OUTPUT
  )

  if(CMAKE_HOSTC_ABI_COMPILED)
    message(STATUS "Detecting HOSTC compiler ABI info - done")
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
      "Detecting HOSTC compiler ABI info compiled with the following output:\n${__CMAKE_HOSTC_ABI_COMPILED_OUTPUT}\n\n"
    )
    parse_host_compiler_abi_info(C ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION}-hosta.internal/CMakeDetermineCompilerABI_HOSTC.bin)
    parse_host_implicit_include_info(C "${__CMAKE_HOSTC_ABI_COMPILED_OUTPUT}")
    parse_host_implicit_link_info(C "${__CMAKE_HOSTC_ABI_COMPILED_OUTPUT}")
  else()
    message(STATUS "Detecting HOSTC compiler ABI info - failed")
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log
      "Detecting HOSTC compiler ABI info failed to compile with the following output:\n${__CMAKE_HOSTC_ABI_COMPILED_OUTPUT}\n\n"
    )
  endif()
endif()

# Set host platform specific default options
set_host_platform_default_options(C)

# Set the host language specific file extensions
set(CMAKE_HOSTC_SOURCE_FILE_EXTENSIONS c m)

# Find BinUtils on the host platform
find_host_binutils(C)

# Configure variables set in this file for fast reload later on
save_host_compiler_preferences(C)

# Add the current host language to the list
list(APPEND ENABLED_HOST_LANGUAGES C)

# Unset temporary variables
unset(__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT)
unset(__CMAKE_HOSTC_ABI_COMPILED_OUTPUT)
