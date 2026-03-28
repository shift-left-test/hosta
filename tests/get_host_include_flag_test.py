#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17)

project(CMakeTest LANGUAGES NONE)

set(ENABLE_HOST_LANGUAGES {languages})
include(cmake/HostBuild.cmake)

get_host_include_flag(OUTPUT)

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_with_host_languages_default(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)

    project(CMakeTest LANGUAGES NONE)

    include(cmake/HostBuild.cmake)

    get_host_include_flag(OUTPUT)

    include(CMakePrintHelpers)
    cmake_print_variables(OUTPUT)
    '''
    testing.write("CMakeLists.txt", content)
    assert 'OUTPUT="-I"' in testing.configure_internal().stdout

def test_with_host_languages_c(testing):
    testing.write("CMakeLists.txt", content.format(languages="C"))
    assert 'OUTPUT="-I"' in testing.configure_internal().stdout

def test_with_host_languages_cxx(testing):
    testing.write("CMakeLists.txt", content.format(languages="CXX"))
    assert 'OUTPUT="-I"' in testing.configure_internal().stdout

def test_with_host_languages_c_cxx(testing):
    testing.write("CMakeLists.txt", content.format(languages="C CXX"))
    assert 'OUTPUT="-I"' in testing.configure_internal().stdout

def test_with_host_languages_none(testing):
    testing.write("CMakeLists.txt", content.format(languages="NONE"))
    assert 'OUTPUT="-I"' in testing.configure_internal().stdout

def test_with_host_languages_none_mixed(testing):
    testing.write("CMakeLists.txt", content.format(languages="C NONE CXX"))
    assert 'OUTPUT="-I"' in testing.configure_internal().stdout
