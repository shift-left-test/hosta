#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
project(CMakeTest LANGUAGES NONE)
include(cmake/HostCompilerUtilities.cmake)
set(CMAKE_HOSTC_COMPILER "{compiler}")
try_host_compile(C
  SOURCE test.c
  TARGET test.bin
  WORKING_DIRECTORY {workspace}
  RESULT_VARIABLE RESULT
  OUTPUT_VARIABLE OUTPUT
)
message(STATUS "RESULT: ${{RESULT}}")
'''

def test_unknown_host_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="unknown", workspace=testing.workspace))
    assert 'RESULT: FALSE' in testing.configure_internal().stdout

def test_compile_invalid_code(testing):
    testing.write("CMakeLists.txt", content.format(compiler="clang", workspace=testing.workspace))
    testing.write("test.c", "int main")
    assert 'RESULT: FALSE' in testing.configure_internal().stdout

def test_compile_valid_code(testing):
    testing.write("CMakeLists.txt", content.format(compiler="clang", workspace=testing.workspace))
    testing.write("test.c", "int main() { }")
    assert 'RESULT: TRUE' in testing.configure_internal().stdout
