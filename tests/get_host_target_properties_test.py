#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(CMakePrintHelpers)
include(cmake/HostBuild.cmake)

add_custom_target(hello COMMAND echo "hello")

set_target_properties(hello PROPERTIES
  HOST_OUTPUT_NAME "output_name"
  HOST_TYPE "type"
  HOST_SOURCES "sources"
  HOST_INTERFACE_INCLUDE_DIRECTORIES "interface_include_directories"
  HOST_INTERFACE_COMPILE_OPTIONS "interface_compile_options"
  HOST_INTERFACE_LINK_OPTIONS "interface_link_options"
)

get_host_target_properties({target}
  NAME name
  OUTPUT_NAME output_name
  TYPE type
  SOURCES sources
  INTERFACE_INCLUDE_DIRECTORIES include_directories
  INTERFACE_COMPILE_OPTIONS compile_options
  INTERFACE_LINK_OPTIONS link_options
)

cmake_print_variables(name output_name type sources include_directories compile_options link_options)
'''

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="unknown"))
    assert 'get_host_target_property() called with non-existent target "unknown".' in testing.configure_internal().stderr

def test_get_host_properties(testing):
    testing.write("CMakeLists.txt", content.format(target="hello"))
    stdout = testing.configure_internal().stdout
    assert 'name="hello"' in stdout
    assert 'output_name="output_name"' in stdout
    assert 'type="type"' in stdout
    assert 'sources="sources"' in stdout
    assert 'include_directories="interface_include_directories"' in stdout
    assert 'compile_options="interface_compile_options"' in stdout
    assert 'link_options="interface_link_options"' in stdout
