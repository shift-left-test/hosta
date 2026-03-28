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

get_host_target_name(OUTPUT "{target}")
cmake_print_variables(OUTPUT)
'''

def test_empty_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target=""))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_target_name_with_unknown_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="ABC::hello"))
    assert 'OUTPUT="ABC::hello"' in testing.configure_internal().stdout

def test_target_name_with_long_unknown_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="ABC::Host::hello"))
    assert 'OUTPUT="ABC::Host::hello"' in testing.configure_internal().stdout

def test_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="hello"))
    assert 'OUTPUT="hello"' in testing.configure_internal().stdout

def test_target_name_with_host_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::hello"))
    assert 'OUTPUT="HOST-hello"' in testing.configure_internal().stdout

def test_target_name_with_nested_host_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::Host::hello"))
    assert 'OUTPUT="HOST-Host::hello"' in testing.configure_internal().stdout
