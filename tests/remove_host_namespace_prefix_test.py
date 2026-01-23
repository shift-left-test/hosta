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

remove_host_namespace_prefix(OUTPUT {target})

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_empty_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target=""))
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="hello"))
    assert 'OUTPUT="hello"' in testing.configure_internal().stdout

def test_non_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="Target::hello"))
    assert 'OUTPUT="Target::hello"' in testing.configure_internal().stdout

def test_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::hello"))
    assert 'OUTPUT="hello"' in testing.configure_internal().stdout

def test_nested_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::Host::hello"))
    assert 'OUTPUT="Host::hello"' in testing.configure_internal().stdout
