# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

# Set the cross compiler toolchain configuration
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_C_COMPILER i686-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER i686-w64-mingw32-g++)
set(CMAKE_FIND_ROOT_PATH /usr/i686-w64-mingw32)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

project(sample LANGUAGES C CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_HOSTC_STANDARD 11)
set(CMAKE_HOSTC_EXTENSIONS ON)

set(CMAKE_HOSTCXX_STANDARD 14)
set(CMAKE_HOSTCXX_EXTENSIONS ON)

include(../cmake/HostTest.cmake)

# Enable CTest
enable_testing()

# External test frameworks
add_subdirectory(external/unity)
add_subdirectory(external/fff)
add_subdirectory(external/gtest)
add_subdirectory(external/cpputest)

# Code coverage (INTERFACE library)
add_host_library(coverage INTERFACE
  COMPILE_OPTIONS PUBLIC -ftest-coverage -fprofile-arcs -O0 -g
  LINK_OPTIONS PUBLIC -fprofile-arcs
)

# --- Expression Calculator Libraries ---

# INTERFACE library: shared error types (header-only)
add_host_library(error INTERFACE
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/error
)

# STATIC library: tokenizer
add_host_library(tokenizer STATIC
  SOURCES tokenizer/tokenizer.c
  INCLUDE_DIRECTORIES
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/tokenizer
  LINK_LIBRARIES PUBLIC Host::error PRIVATE Host::coverage
)

# STATIC library: parser
add_host_library(parser STATIC
  SOURCES parser/parser.c
  INCLUDE_DIRECTORIES
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/parser
  LINK_LIBRARIES PUBLIC Host::tokenizer Host::error PRIVATE Host::coverage
)

# SHARED library: evaluator (demonstrates VERSION/SOVERSION)
add_host_library(eval SHARED
  SOURCES evaluator/evaluator.c
  INCLUDE_DIRECTORIES
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/evaluator
  LINK_LIBRARIES PUBLIC Host::parser Host::tokenizer Host::error PRIVATE Host::coverage
  VERSION 1.0.0
  SOVERSION 1
)

# Host executable: expression calculator CLI
add_host_executable(calc
  SOURCES calculator/main.c
  LINK_LIBRARIES PRIVATE Host::eval Host::parser Host::tokenizer Host::error
)

# --- Tests ---
add_subdirectory(test)
