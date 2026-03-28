#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)

transform_host_arguments(OUTPUT "{data}" {args})

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_empty_input(testing):
    testing.write("CMakeLists.txt", content.format(data="", args=""))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_single_data(testing):
    testing.write("CMakeLists.txt", content.format(data="hello", args=""))
    assert 'OUTPUT="hello"' in testing.configure_internal().stdout

def test_multiple_data(testing):
    testing.write("CMakeLists.txt", content.format(data="hello;world", args=""))
    assert 'OUTPUT="hello;world"' in testing.configure_internal().stdout

def test_prepend(testing):
    testing.write("CMakeLists.txt", content.format(data="hello;world", args="PREPEND -I"))
    assert 'OUTPUT="-Ihello;-Iworld"' in testing.configure_internal().stdout

def test_skip_generator_expression(testing):
    testing.write("CMakeLists.txt", content.format(data="hello;-I$<JOIN:$<TARGET_PROPERTY:module,HOST_INTERFACE_INCLUDE_DIRECTORIES>,$<SEMICOLON>-I>;world", args="PREPEND -I"))
    assert 'OUTPUT="-Ihello;-I$<JOIN:$<TARGET_PROPERTY:module,HOST_INTERFACE_INCLUDE_DIRECTORIES>,$<SEMICOLON>-I>;-Iworld"' in testing.configure_internal().stdout
