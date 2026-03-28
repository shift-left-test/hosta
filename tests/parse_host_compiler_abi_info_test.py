#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
project(CMakeTest LANGUAGES NONE)
include(cmake/HostCompilerUtilities.cmake)
parse_host_compiler_abi_info(C {path})
message(STATUS "CMAKE_HOSTC_COMPILER_ABI: ${{CMAKE_HOSTC_COMPILER_ABI}}")
'''

def test_parse_unknown_file(testing):
    testing.write("CMakeLists.txt", content.format(path="unknown.file"))
    assert 'CMAKE_HOSTC_COMPILER_ABI: \n' in testing.configure_internal().stdout

def test_parse_missing_abi_info(testing):
    testing.write("CMakeLists.txt", content.format(path="test.bin"))
    testing.write("test.bin", "INFO:a[]\nINFO:b[]\n")
    assert 'CMAKE_HOSTC_COMPILER_ABI: \n' in testing.configure_internal().stdout

def test_parse_abi_info(testing):
    testing.write("CMakeLists.txt", content.format(path="test.bin"))
    testing.write("test.bin", "INFO:a[]\nINFO:b[]\nINFO:abi[hello]\n")
    assert 'CMAKE_HOSTC_COMPILER_ABI: hello\n' in testing.configure_internal().stdout
