#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostCompilerUtilities.cmake)

set(CMAKE_HOSTX_COMPILER_LIST {compiler})

find_host_compiler(X)

include(CMakePrintHelpers)
cmake_print_variables(CMAKE_HOSTX_COMPILER)
'''

def test_unknown_host_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="unknown"))
    assert 'CMAKE_HOSTX_COMPILER="CMAKE_HOSTX_COMPILER-NOTFOUND' in testing.configure_internal().stdout

def test_known_host_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="clang"))
    assert 'CMAKE_HOSTX_COMPILER="/usr/bin/clang' in testing.configure_internal().stdout
