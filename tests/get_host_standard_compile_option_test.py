#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)

get_host_standard_compile_option(C OUTPUT)

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_default_option(testing):
    testing.write("CMakeLists.txt", content)
    assert 'OUTPUT=""' in testing.configure_internal().stdout

def test_unknown_version(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_HOSTC_STANDARD=12345']
    assert "HOSTC_STANDARD is set to invalid value '12345'" in testing.configure_internal(options).stderr

def test_default_version_with_extension_on(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_HOSTC_EXTENSIONS=ON']
    assert 'OUTPUT=""' in testing.configure_internal(options).stdout

def test_valid_version_with_default_extension(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_HOSTC_STANDARD=11']
    assert 'OUTPUT="-std=gnu11"' in testing.configure_internal(options).stdout

def test_valid_version_with_extension_off(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_HOSTC_STANDARD=11 -DCMAKE_HOSTC_EXTENSIONS=OFF']
    assert 'OUTPUT="-std=c11"' in testing.configure_internal(options).stdout

def test_valid_version_with_extension_on(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_HOSTC_STANDARD=11 -DCMAKE_HOSTC_EXTENSIONS=ON']
    assert 'OUTPUT="-std=gnu11"' in testing.configure_internal(options).stdout
