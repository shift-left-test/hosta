#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


def test_host_compiler_info(testing):
    testing.configure(c_compiler_list="gcc")
    compiler_info = testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTCCompiler.cmake")
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/gcc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ID "GNU")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_VERSION "13.3.0")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_STANDARD_COMPUTED_DEFAULT "17")' in compiler_info
    assert 'set(CMAKE_HOSTC_PLATFORM_ID "Linux")' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/13/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/13;/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
    assert 'set(CMAKE_HOSTC_VERBOSE_FLAG "-v")' in compiler_info
    assert 'set(CMAKE_HOSTC_SOURCE_FILE_EXTENSIONS "c;m")' in compiler_info
    assert 'set(CMAKE_HOSTC_OUTPUT_EXTENSION ".o")' in compiler_info
    assert 'set(CMAKE_HOSTC_EXECUTABLE_SUFFIX "")' in compiler_info
    assert 'set(CMAKE_HOSTC_STATIC_LIBRARY_PREFIX "lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_STATIC_LIBRARY_SUFFIX ".a")' in compiler_info
    assert 'set(CMAKE_HOSTC_AR "/usr/bin/ar")' in compiler_info
    assert 'set(CMAKE_HOSTC_RANLIB "/usr/bin/ranlib")' in compiler_info
    assert 'set(CMAKE_INCLUDE_FLAG_HOSTC "-I")' in compiler_info
    assert 'set(CMAKE_INCLUDE_SYSTEM_FLAG_HOSTC "-isystem ")' in compiler_info
    assert 'set(CMAKE_HOSTC11_STANDARD_COMPILE_OPTION "-std=c11")' in compiler_info
    assert 'set(CMAKE_HOSTC11_EXTENSION_COMPILE_OPTION "-std=gnu11")' in compiler_info
