#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_enable_host_languages_default(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    '''
    testing.write("CMakeLists.txt", content)
    stdout = testing.configure_internal().stdout
    assert 'Check for working HOSTC compiler: /usr/bin/cc -- works' in stdout
    assert 'Check for working HOSTCXX compiler: /usr/bin/c++ -- works' in stdout

def test_enable_host_languages_c(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    set(ENABLE_HOST_LANGUAGES C)
    include(cmake/HostBuild.cmake)
    '''
    testing.write("CMakeLists.txt", content)
    stdout = testing.configure_internal().stdout
    assert 'Check for working HOSTC compiler: /usr/bin/cc -- works' in stdout
    assert not 'Check for working HOSTCXX compiler: /usr/bin/c++ -- works' in stdout

def test_enable_host_languages_cxx(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    set(ENABLE_HOST_LANGUAGES CXX)
    include(cmake/HostBuild.cmake)
    '''
    testing.write("CMakeLists.txt", content)
    stdout = testing.configure_internal().stdout
    assert not 'Check for working HOSTC compiler: /usr/bin/cc -- works' in stdout
    assert 'Check for working HOSTCXX compiler: /usr/bin/c++ -- works' in stdout

def test_enable_host_languages_c_cxx(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    set(ENABLE_HOST_LANGUAGES C CXX)
    include(cmake/HostBuild.cmake)
    '''
    testing.write("CMakeLists.txt", content)
    stdout = testing.configure_internal().stdout
    assert 'Check for working HOSTC compiler: /usr/bin/cc -- works' in stdout
    assert 'Check for working HOSTCXX compiler: /usr/bin/c++ -- works' in stdout

def test_enable_host_languages_none(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    set(ENABLE_HOST_LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    '''
    testing.write("CMakeLists.txt", content)
    process = testing.configure_internal()
    stdout = process.stdout
    stderr = process.stderr
    assert not 'Check for working HOSTC compiler: /usr/bin/cc -- works' in stdout
    assert not 'Check for working HOSTCXX compiler: /usr/bin/c++ -- works' in stdout
    assert not 'No CMAKE_HOSTNONE_COMPILER could be found.' in stderr

def test_enable_host_languages_none_mixed(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    set(ENABLE_HOST_LANGUAGES C NONE CXX)
    include(cmake/HostBuild.cmake)
    '''
    testing.write("CMakeLists.txt", content)
    process = testing.configure_internal()
    stdout = process.stdout
    stderr = process.stderr
    assert 'Check for working HOSTC compiler: /usr/bin/cc -- works' in stdout
    assert 'Check for working HOSTCXX compiler: /usr/bin/c++ -- works' in stdout
    assert not 'No CMAKE_HOSTNONE_COMPILER could be found.' in stderr

def test_enable_host_languages_unknown(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17)
    project(CMakeTest LANGUAGES NONE)
    set(ENABLE_HOST_LANGUAGES HELLO)
    include(cmake/HostBuild.cmake)
    '''
    testing.write("CMakeLists.txt", content)
    assert 'No CMAKE_HOSTHELLO_COMPILER could be found.' in testing.configure_internal().stderr
