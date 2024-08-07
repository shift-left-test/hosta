#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(CMakePrintHelpers)
include(cmake/HostBuild.cmake)

add_custom_target(hello COMMAND echo "hello")

set_host_target_properties({target}
  TYPE "type"
  SOURCES "sources"
  INTERFACE_INCLUDE_DIRECTORIES "interface_include_directories"
  INTERFACE_COMPILE_OPTIONS "interface_compile_options"
  INTERFACE_LINK_OPTIONS "interface_link_options"
)

get_host_target_properties(hello
  NAME name
  TYPE type
  SOURCES sources
  INTERFACE_INCLUDE_DIRECTORIES include_directories
  INTERFACE_COMPILE_OPTIONS compile_options
  INTERFACE_LINK_OPTIONS link_options
)

cmake_print_variables(name type target_file sources include_directories compile_options link_options)
'''

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="unknown"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'set_host_target_property() called with non-existent target "unknown".' in testing.configure_internal(options).stderr

def test_get_set_properties(testing):
    testing.write("CMakeLists.txt", content.format(target="hello"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    stdout = testing.configure_internal(options).stdout
    assert 'name="hello"' in stdout
    assert 'type="type"' in stdout
    assert 'sources="sources"' in stdout
    assert 'include_directories="interface_include_directories"' in stdout
    assert 'compile_options="interface_compile_options"' in stdout
    assert 'link_options="interface_link_options"' in stdout
