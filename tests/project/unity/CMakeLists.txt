# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

add_host_library(unity STATIC
  SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/unity.c
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_LIST_DIR}
  COMPILE_OPTIONS PUBLIC -DUNITY_INCLUDE_DOUBLE
)

add_host_library(unity-fixture STATIC
  SOURCES unity_fixture.c
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_LIST_DIR}
  COMPILE_OPTIONS PUBLIC -DUNITY_FIXTURE_NO_EXTRAS
)
