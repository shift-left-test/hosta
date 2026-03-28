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

get_host_absolute_paths(PATHS "{paths}")
cmake_print_variables(PATHS)
'''

def test_empty_path(testing):
    testing.write("CMakeLists.txt", content.format(paths=""))
    assert 'PATHS=""' in testing.configure_internal().stdout

def test_one_path(testing):
    testing.write("CMakeLists.txt", content.format(paths="first"))
    assert f'PATHS="{testing.workspace}/first"' in testing.configure_internal().stdout

def test_multiple_paths(testing):
    testing.write("CMakeLists.txt", content.format(paths="first;second"))
    assert f'PATHS="{testing.workspace}/first;{testing.workspace}/second"' in testing.configure_internal().stdout

def test_generator_expression(testing):
    testing.write("CMakeLists.txt", content.format(paths="first;$<TARGET_PROPERTY:hello,SOURCES>;second"))
    assert f'PATHS="{testing.workspace}/first;$<TARGET_PROPERTY:hello,SOURCES>;{testing.workspace}/second"' in testing.configure_internal().stdout
