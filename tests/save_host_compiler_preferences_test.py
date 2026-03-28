#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostCompilerUtilities.cmake)

set(CMAKE_HOSTX_COMPILER "hello")

set(CMAKE_HOSTX90_STANDARD_COMPILE_OPTION "x90")
set(CMAKE_HOSTX26_EXTENSION_COMPILE_OPTION "x26")
set(CMAKE_HOSTX27_STANDARD_COMPILE_OPTION "x27")

save_host_compiler_preferences(X)
'''

def test_save_file(testing):
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    assert 'set(CMAKE_HOSTX_COMPILER "hello")' in testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTXCompiler.cmake")

def test_valid_language_standard_versions(testing):
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    assert 'set(CMAKE_HOSTX90_STANDARD_COMPILE_OPTION "x90")' in testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTXCompiler.cmake")
    assert 'set(CMAKE_HOSTX26_EXTENSION_COMPILE_OPTION "x26")' in testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTXCompiler.cmake")

def test_invalid_language_standard_versions(testing):
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    assert 'set(CMAKE_HOSTX27_STANDARD_COMPILE_OPTION "x27")' not in testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTXCompiler.cmake")

def test_save_shared_library_variables(testing):
    content = '''
    cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostCompilerUtilities.cmake)

    set(CMAKE_HOSTX_COMPILER "hello")
    set(CMAKE_HOSTX_SHARED_LIBRARY_PREFIX "lib")
    set(CMAKE_HOSTX_SHARED_LIBRARY_SUFFIX ".so")
    set(CMAKE_HOSTX_COMPILE_OPTIONS_PIC "-fPIC")
    set(CMAKE_HOSTX_SHARED_LIBRARY_SONAME_FLAG "-Wl,-soname,")
    set(CMAKE_HOSTX_SHARED_LIBRARY_RUNTIME_FLAG "-Wl,-rpath,")
    set(CMAKE_HOSTX_SHARED_LIBRARY_CREATE_FLAGS "-shared")

    save_host_compiler_preferences(X)
    '''
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    saved = testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTXCompiler.cmake")
    assert 'set(CMAKE_HOSTX_SHARED_LIBRARY_PREFIX "lib")' in saved
    assert 'set(CMAKE_HOSTX_SHARED_LIBRARY_SUFFIX ".so")' in saved
    assert 'set(CMAKE_HOSTX_COMPILE_OPTIONS_PIC "-fPIC")' in saved
    assert 'set(CMAKE_HOSTX_SHARED_LIBRARY_SONAME_FLAG "-Wl,-soname,")' in saved
    assert 'set(CMAKE_HOSTX_SHARED_LIBRARY_RUNTIME_FLAG "-Wl,-rpath,")' in saved
    assert 'set(CMAKE_HOSTX_SHARED_LIBRARY_CREATE_FLAGS "-shared")' in saved
