#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)

add_custom_target({first} COMMAND echo "first")
add_custom_target({second} COMMAND echo "second")

add_host_dependencies({command})
'''

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="second", command="unknown unknown"))
    assert 'Cannot add target-level dependencies to non-existent target "unknown".' in testing.configure_internal().stderr

def test_unknown_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="second", command="first unknown"))
    assert 'The dependency target "unknown" of target "first" does not exist.' in testing.configure_internal().stderr

def test_plain_target_depend_names(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="second", command="first second"))
    testing.configure_internal().check_returncode()

def test_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="HOST-first", second="second", command="Host::first second"))
    testing.configure_internal().check_returncode()

def test_host_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="HOST-second", command="first Host::second"))
    testing.configure_internal().check_returncode()

def test_host_target_and_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="HOST-first", second="HOST-second", command="Host::first Host::second"))
    testing.configure_internal().check_returncode()

def test_host_namespace_with_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="HOST-second", command="Host::first Host::second"))
    assert 'Cannot add target-level dependencies to non-existent target "HOST-first".' in testing.configure_internal().stderr

def test_host_namespace_with_plain_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="HOST-first", second="second", command="Host::first Host::second"))
    assert 'The dependency target "HOST-second" of target "HOST-first" does not exist.' in testing.configure_internal().stderr

def test_host_multiple_dependencies(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_custom_target(HOST-first COMMAND echo "first")
    add_custom_target(HOST-second COMMAND echo "second")
    add_custom_target(HOST-third COMMAND echo "third")
    add_host_dependencies(Host::first "Host::second;Host::third")
    '''
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("HOST-first", verbose=True).stdout
    assert 'Built target HOST-first' in stdout
    assert 'Built target HOST-second' in stdout
    assert 'Built target HOST-third' in stdout
