#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(CMakePrintHelpers)
include(cmake/HostCompilerUtilities.cmake)

set(CMAKE_HOSTC_COMPILER_ID {compiler})
set(CMAKE_HOSTC_PLATFORM_ID {platform})
set(CMAKE_GENERATOR {generator})

set_host_platform_default_options(C)

cmake_print_variables(
  CMAKE_HOSTC_OUTPUT_EXTENSION
  CMAKE_HOSTC_EXECUTABLE_SUFFIX
  CMAKE_HOSTC_STATIC_LIBRARY_PREFIX
  CMAKE_HOSTC_STATIC_LIBRARY_SUFFIX
  CMAKE_GENERATOR
)
'''

def test_unsupported_host_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="MSVC", platform="Linux", generator="Ninja"))
    assert "Builds based on 'MSVC' compiler not supported." in testing.configure_internal().stderr

def test_unsupported_host_generator(testing):
    testing.write("CMakeLists.txt", content.format(compiler="Clang", platform="Linux", generator="Visual\\ Studio\\ 16\\ 2019"))
    assert "Builds based on 'Visual Studio 16 2019' generator not supported." in testing.configure_internal().stderr

def test_unknown_host_platform(testing):
    testing.write("CMakeLists.txt", content.format(compiler="Clang", platform="unknown", generator="Ninja"))
    assert "Builds hosted on 'unknown' not supported." in testing.configure_internal().stderr

def test_cygwin(testing):
    testing.write("CMakeLists.txt", content.format(compiler="Clang", platform="CYGWIN", generator="Ninja"))
    stdout = testing.configure_internal().stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".obj"' in stdout
    assert 'CMAKE_HOSTC_EXECUTABLE_SUFFIX=".exe"' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_PREFIX=""' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_SUFFIX=".lib"' in stdout

def test_linux(testing):
    testing.write("CMakeLists.txt", content.format(compiler="Clang", platform="Linux", generator="Ninja"))
    stdout = testing.configure_internal().stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".o"' in stdout
    assert 'CMAKE_HOSTC_EXECUTABLE_SUFFIX=""' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_PREFIX="lib"' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_SUFFIX=".a"' in stdout

def test_mingw(testing):
    testing.write("CMakeLists.txt", content.format(compiler="Clang", platform="MinGW", generator="Ninja"))
    stdout = testing.configure_internal().stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".obj"' in stdout
    assert 'CMAKE_HOSTC_EXECUTABLE_SUFFIX=".exe"' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_PREFIX=""' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_SUFFIX=".lib"' in stdout

def test_windows(testing):
    testing.write("CMakeLists.txt", content.format(compiler="Clang", platform="Windows", generator="Ninja"))
    stdout = testing.configure_internal().stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".obj"' in stdout
    assert 'CMAKE_HOSTC_EXECUTABLE_SUFFIX=".exe"' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_PREFIX=""' in stdout
    assert 'CMAKE_HOSTC_STATIC_LIBRARY_SUFFIX=".lib"' in stdout
