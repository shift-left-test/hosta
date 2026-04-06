# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

# Set the directory of the current file
if(NOT _HOSTA_BASE_DIR)
  set(_HOSTA_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")
endif()

# The compiler configuration was forced by the user.
# Assume the user has configured all compiler information
if(CMAKE_HOSTCXX_COMPILER_FORCED)
  set(CMAKE_HOSTCXX_COMPILER_WORKS TRUE)
  list(APPEND ENABLED_HOST_LANGUAGES CXX)
  return()
endif()

include(${_HOSTA_BASE_DIR}/HostCompilerUtilities.cmake)

# Load host compiler preferences
load_host_compiler_preferences(CXX)

# Assume that the host compiler works properly
if(CMAKE_HOSTCXX_COMPILER_WORKS)
  if(NOT EXISTS "${CMAKE_HOSTCXX_COMPILER}")
    message(WARNING "Cached HOSTCXX compiler '${CMAKE_HOSTCXX_COMPILER}' no longer exists. Re-detecting...")
  else()
    list(APPEND ENABLED_HOST_LANGUAGES CXX)
    return()
  endif()
endif()

include(CMakeTestCompilerCommon)

# List compilers to try
if(NOT CMAKE_HOSTCXX_COMPILER_LIST)
  set(CMAKE_HOSTCXX_COMPILER_LIST c++ g++ clang++)
endif()

find_host_compiler(CXX)

# Check if a host compiler is available
if(NOT CMAKE_HOSTCXX_COMPILER)
  host_logging_error(
    "The CMAKE_HOSTCXX_COMPILER:"
    "  ${CMAKE_HOSTCXX_COMPILER_LIST}\n"
    "is not a full path and was not found in the PATH."
  )
endif()

# Build a small source file to identify the compiler.
find_host_compiler_id(CXX)

# Test if the host compiler can compile the most basic of programs.
# If not, a fatal error is set and stops processing commands.
PrintTestCompilerStatus("HOSTCXX" "")

file(WRITE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/testHOSTCXXCompiler.cpp
  "#ifndef __cplusplus\n"
  "# error \"The CMAKE_HOSTCXX_COMPILER is set to a C compiler\"\n"
  "#endif\n"
  "int main(){return 0;}\n"
)

try_host_compile(CXX
  SOURCE testHOSTCXXCompiler.cpp
  TARGET testHOSTCXXCompiler.bin
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp
  RESULT_VARIABLE CMAKE_HOSTCXX_COMPILER_WORKS
  OUTPUT_VARIABLE __CMAKE_HOSTCXX_COMPILER_WORKS_OUTPUT
)

if(NOT CMAKE_HOSTCXX_COMPILER_WORKS)
  PrintTestCompilerStatus("HOSTCXX" " -- broken")

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log
    "Determining if the HOSTCXX compiler works failed with "
    "the following output:\n${__CMAKE_HOSTCXX_COMPILER_WORKS_OUTPUT}\n\n"
  )
  string(REPLACE "\n" "\n  " _output "${__CMAKE_HOSTCXX_COMPILER_WORKS_OUTPUT}")
  message(FATAL_ERROR "The HOSTCXX compiler\n  \"${CMAKE_HOSTCXX_COMPILER}\"\n"
    "is not able to compile a simple test program.\nIt fails "
    "with the following output:\n  ${_output}\n\n"
    "CMake will not be able to correctly generate this project."
  )
else()
  PrintTestCompilerStatus("HOSTCXX" " -- works")

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Determining if the HOSTCXX compiler works passed with "
    "the following output:\n${__CMAKE_HOSTCXX_COMPILER_WORKS_OUTPUT}\n\n"
  )

  # Try to identify the ABI
  try_host_compile(CXX
    SOURCE ${CMAKE_ROOT}/Modules/CMakeCXXCompilerABI.cpp
    TARGET CMakeDetermineCompilerABI_HOSTCXX.bin
    COMPILE_OPTIONS ${CMAKE_HOSTCXX_VERBOSE_FLAG}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION}-hosta.internal
    RESULT_VARIABLE CMAKE_HOSTCXX_ABI_COMPILED
    OUTPUT_VARIABLE __CMAKE_HOSTCXX_ABI_COMPILED_OUTPUT
  )

  if(CMAKE_HOSTCXX_ABI_COMPILED)
    message(STATUS "Detecting HOSTCXX compiler ABI info - done")
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
      "Detecting HOSTCXX compiler ABI info compiled with the following output:\n${__CMAKE_HOSTCXX_ABI_COMPILED_OUTPUT}\n\n"
    )
    parse_host_compiler_abi_info(CXX ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION}-hosta.internal/CMakeDetermineCompilerABI_HOSTCXX.bin)
    parse_host_implicit_include_info(CXX "${__CMAKE_HOSTCXX_ABI_COMPILED_OUTPUT}")
    parse_host_implicit_link_info(CXX "${__CMAKE_HOSTCXX_ABI_COMPILED_OUTPUT}")
  else()
    message(STATUS "Detecting HOSTCXX compiler ABI info - failed")
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log
      "Detecting HOSTCXX compiler ABI info failed to compile with the following output:\n${__CMAKE_HOSTCXX_ABI_COMPILED_OUTPUT}\n\n"
    )
  endif()
endif()

# Set host platform specific default options
set_host_platform_default_options(CXX)

# Set the host language specific file extensions
set(CMAKE_HOSTCXX_SOURCE_FILE_EXTENSIONS C M c++ cc cpp cxx m mm CPP)

# Find BinUtils on the host platform
find_host_binutils(CXX)

# Configure variables set in this file for fast reload later on
save_host_compiler_preferences(CXX)

# Add the current host language to the list
list(APPEND ENABLED_HOST_LANGUAGES CXX)

# Unset temporary variables
unset(__CMAKE_HOSTCXX_COMPILER_WORKS_OUTPUT)
unset(__CMAKE_HOSTCXX_ABI_COMPILED_OUTPUT)
