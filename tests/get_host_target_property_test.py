#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(CMakePrintHelpers)
include(cmake/HostBuild.cmake)

add_custom_target(hello COMMAND echo "hello")
set_target_properties(hello PROPERTIES {key} "{value}")
get_host_target_property(OUTPUT {target} {property})
cmake_print_variables(OUTPUT)
'''

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", content.format(key="HOST_SOURCES", value="aaa", target="unknown", property="HOST_SOURCES"))
    assert 'get_host_target_property() called with non-existent target "unknown".' in testing.configure_internal().stderr

def test_unknown_property_name(testing):
    testing.write("CMakeLists.txt", content.format(key="HOST_SOURCES", value="aaa", target="hello", property="unknown"))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_get_original_property(testing):
    testing.write("CMakeLists.txt", content.format(key="HOST_SOURCES", value="aaa", target="hello", property="NAME"))
    assert 'OUTPUT="hello"' in testing.configure_internal().stdout

def test_get_empty_host_property(testing):
    testing.write("CMakeLists.txt", content.format(key="HOST_SOURCES", value="aaa", target="hello", property="HOST_TYPE"))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_get_host_property_single_value(testing):
    testing.write("CMakeLists.txt", content.format(key="HOST_SOURCES", value="abc", target="hello", property="HOST_SOURCES"))
    assert 'OUTPUT="abc"' in testing.configure_internal().stdout

def test_get_host_property_multi_values(testing):
    testing.write("CMakeLists.txt", content.format(key="HOST_SOURCES", value="a;b;c", target="hello", property="HOST_SOURCES"))
    assert 'OUTPUT="a;b;c"' in testing.configure_internal().stdout
