#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostCompilerUtilities.cmake)

load_host_compiler_preferences(X)

message(STATUS "load_host_compiler_preferences(X): ${DATA}")
'''

def test_unknown_file(testing):
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    assert "load_host_compiler_preferences(X): hello" not in testing.configure_internal().stdout

def test_load_file(testing):
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    testing.write("build/CMakeFiles/3.28.3-hosta.internal/CMakeHOSTXCompiler.cmake", 'set(DATA "hello")\n')
    assert "load_host_compiler_preferences(X): hello" in testing.configure_internal().stdout
