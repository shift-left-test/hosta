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
set_target_properties(hello PROPERTIES {key} "{value}")
get_host_target_property(OUTPUT {target} {property})
cmake_print_variables(OUTPUT)
'''

def make_lists(key="HOST_SOURCES", value="aaa", target="hello", property="HOST_SOURCES"):
    # Each test overrides only the field it exercises; the rest stay at the
    # common defaults (target "hello", property HOST_SOURCES) so the intent of
    # every test reads at a glance.
    return content.format(key=key, value=value, target=target, property=property)

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", make_lists(target="unknown"))
    assert 'get_host_target_property() called with non-existent target "unknown".' in testing.configure_internal().stderr

def test_unknown_property_name(testing):
    testing.write("CMakeLists.txt", make_lists(property="unknown"))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_get_original_property(testing):
    testing.write("CMakeLists.txt", make_lists(property="NAME"))
    assert 'OUTPUT="hello"' in testing.configure_internal().stdout

def test_get_empty_host_property(testing):
    testing.write("CMakeLists.txt", make_lists(property="HOST_TYPE"))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_get_host_property_single_value(testing):
    testing.write("CMakeLists.txt", make_lists(value="abc"))
    assert 'OUTPUT="abc"' in testing.configure_internal().stdout

def test_get_host_property_multi_values(testing):
    testing.write("CMakeLists.txt", make_lists(value="a;b;c"))
    assert 'OUTPUT="a;b;c"' in testing.configure_internal().stdout

def test_get_host_property_falsy_value_zero(testing):
    testing.write("CMakeLists.txt", make_lists(key="HOST_SOVERSION", value="0", property="HOST_SOVERSION"))
    assert 'OUTPUT="0"' in testing.configure_internal().stdout

def test_get_host_property_falsy_value_false(testing):
    testing.write("CMakeLists.txt", make_lists(key="HOST_VERSION", value="FALSE", property="HOST_VERSION"))
    assert 'OUTPUT="FALSE"' in testing.configure_internal().stdout
