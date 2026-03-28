#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)

add_custom_command(OUTPUT first COMMAND echo "first")
add_custom_command(OUTPUT second COMMAND echo "second")

add_custom_target(A DEPENDS first)
add_custom_target(HOST-B DEPENDS second)

add_host_custom_target({first} DEPENDS {second})
'''

def test_unknown_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="TARGET", second="unknown"))
    testing.configure_internal().check_returncode()
    assert 'No rule to make target' in testing.cmake("TARGET").stderr

def test_existing_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="A", second="unknown"))
    assert 'add_custom_target cannot create target "A"' in testing.configure_internal().stderr

def test_existing_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="Host::B", second="unknown"))
    assert 'add_custom_target cannot create target "HOST-B"' in testing.configure_internal().stderr

def test_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="TARGET", second="A"))
    testing.configure_internal().check_returncode()
    assert 'Built target A' in testing.cmake("TARGET").stdout

def test_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="Host::TARGET", second="A"))
    testing.configure_internal().check_returncode()
    assert 'Built target A' in testing.cmake("HOST-TARGET").stdout

def test_host_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="TARGET", second="Host::B"))
    testing.configure_internal().check_returncode()
    assert 'Built target HOST-B' in testing.cmake("TARGET").stdout

def test_no_depends(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_custom_target(hello)
    if(TARGET hello)
      message(STATUS "hello exists")
    else()
      message(STATUS "hello not exists")
    endif()
    '''
    testing.write("CMakeLists.txt", content)
    assert 'hello exists' in testing.configure_internal().stdout

def test_multiple_dependencies(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_custom_target(HOST-second COMMAND echo "second")
    add_custom_target(HOST-third COMMAND echo "third")
    add_host_custom_target(Host::first DEPENDS "Host::second;Host::third")
    '''
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("HOST-first", verbose=True).stdout
    assert 'Built target HOST-first' in stdout
    assert 'Built target HOST-second' in stdout
    assert 'Built target HOST-third' in stdout
