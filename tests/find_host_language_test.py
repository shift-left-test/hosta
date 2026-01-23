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

find_host_language(OUTPUT "{sources}")

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_empty_source_file(testing):
    testing.write("CMakeLists.txt", content.format(sources=""))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_unknown_source_file_extension(testing):
    testing.write("CMakeLists.txt", content.format(sources="world.x"))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_unknown_source_file_extensions(testing):
    testing.write("CMakeLists.txt", content.format(sources="hello.c world.x"))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_c_source_file_extensions(testing):
    testing.write("CMakeLists.txt", content.format(sources="hello.c world.m"))
    assert 'OUTPUT="C"' in testing.configure_internal().stdout
