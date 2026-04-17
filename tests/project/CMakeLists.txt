# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

option(WITH_CROSS_TOOLCHAIN "Enable cross toolchain" ON)

if(WITH_CROSS_TOOLCHAIN)
  # the name of the target operating system
  set(CMAKE_SYSTEM_NAME Windows)

  # which compilers to use for C and C++
  set(CMAKE_C_COMPILER i686-w64-mingw32-gcc)
  set(CMAKE_CXX_COMPILER i686-w64-mingw32-g++)

  # where is the target environment located
  set(CMAKE_FIND_ROOT_PATH /usr/i686-w64-mingw32)

  # adjust the default behavior of the FIND_XXX() commands:
  # search programs in the host environment
  set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

  # search headers and libraries in the target environment
  set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
  set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
endif()

project(host-test LANGUAGES C CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(cmake/HostTest.cmake)

add_custom_target(hello
  COMMAND echo "hello"
)

add_host_library(coverage INTERFACE
  COMPILE_OPTIONS PUBLIC -ftest-coverage -fprofile-arcs -O0
  LINK_OPTIONS PUBLIC -fprofile-arcs
)

add_host_library(hostc_options INTERFACE
  COMPILE_OPTIONS PUBLIC ${EXTRA_HOSTC_COMPILE_OPTIONS}
  LINK_OPTIONS PUBLIC ${EXTRA_HOSTC_LINK_OPTIONS}
)

add_host_library(hostcxx_options INTERFACE
  COMPILE_OPTIONS PUBLIC ${EXTRA_HOSTCXX_COMPILE_OPTIONS}
  LINK_OPTIONS PUBLIC ${EXTRA_HOSTCXX_LINK_OPTIONS}
)

add_host_executable(unity_test
  SOURCES calculator/calc.c test/unity_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_LIST_DIR}/calculator ${CMAKE_CURRENT_LIST_DIR}/test
  LINK_LIBRARIES PRIVATE Host::unity Host::coverage Host::hostc_options
  DEPENDS hello
)

add_host_test(Host::unity_test PREFIX ${HOST_TEST_PREFIX})

add_subdirectory(calculator)
add_subdirectory(test)
add_subdirectory(relative_path_test)
add_subdirectory(external/unity)
add_subdirectory(external/gtest)
add_subdirectory(external/cpputest)
