#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest)

include(cmake/HostCompilerUtilities.cmake)

set(CMAKE_HOSTW_COMPILER_LIST unknown)
set(CMAKE_HOSTX_COMPILER_LIST clang)

find_host_compiler(X)

message(STATUS "CMAKE_HOSTW_COMPILER: ${CMAKE_HOSTW_COMPILER}")
message(STATUS "CMAKE_HOSTX_COMPILER: ${CMAKE_HOSTX_COMPILER}")
'''

def test_unknown_host_compiler(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOSTW_COMPILER: \n' in testing.configure_internal(options).stdout

def test_known_host_compiler(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOSTX_COMPILER: /usr/bin/clang' in testing.configure_internal(options).stdout
