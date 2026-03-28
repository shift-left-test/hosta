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

get_host_target_names(OUTPUT "{target}")
cmake_print_variables(OUTPUT)
'''

def test_empty_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target=""))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_target_name_with_unknown_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="ABC::hello;ABC::world"))
    assert 'OUTPUT="ABC::hello;ABC::world"' in testing.configure_internal().stdout

def test_target_name_with_long_unknown_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="ABC::Host::hello;ABC::Host::world"))
    assert 'OUTPUT="ABC::Host::hello;ABC::Host::world"' in testing.configure_internal().stdout

def test_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="hello;world"))
    assert 'OUTPUT="hello;world"' in testing.configure_internal().stdout

def test_target_name_with_host_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::hello;Host::world"))
    assert 'OUTPUT="HOST-hello;HOST-world"' in testing.configure_internal().stdout

def test_target_name_with_nested_host_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::Host::hello;Host::Host::world"))
    assert 'OUTPUT="HOST-Host::hello;HOST-Host::world"' in testing.configure_internal().stdout
