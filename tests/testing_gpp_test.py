#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


def test_host_compiler_info(testing):
    testing.configure(cpp_compiler_list="g++")
    compiler_info = testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTCXXCompiler.cmake")
    assert 'set(CMAKE_HOSTCXX_COMPILER "/usr/bin/g++")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_ID "GNU")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_VERSION "13.3.0")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTCXX_STANDARD_COMPUTED_DEFAULT "17")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_PLATFORM_ID "Linux")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_INCLUDE_DIRECTORIES "/usr/include/c++/13;/usr/include/x86_64-linux-gnu/c++/13;/usr/include/c++/13/backward;/usr/lib/gcc/x86_64-linux-gnu/13/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_LIBRARIES "stdc++;m;gcc_s;gcc;c;gcc_s;gcc")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/13;/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_VERBOSE_FLAG "-v")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_SOURCE_FILE_EXTENSIONS "C;M;c++;cc;cpp;cxx;m;mm;CPP")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_OUTPUT_EXTENSION ".o")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_EXECUTABLE_SUFFIX "")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_STATIC_LIBRARY_PREFIX "lib")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_STATIC_LIBRARY_SUFFIX ".a")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_AR "/usr/bin/ar")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_RANLIB "/usr/bin/ranlib")' in compiler_info
    assert 'set(CMAKE_INCLUDE_FLAG_HOSTCXX "-I")' in compiler_info
    assert 'set(CMAKE_INCLUDE_SYSTEM_FLAG_HOSTCXX "-isystem ")' in compiler_info
    assert 'set(CMAKE_HOSTCXX11_STANDARD_COMPILE_OPTION "-std=c++11")' in compiler_info
    assert 'set(CMAKE_HOSTCXX11_EXTENSION_COMPILE_OPTION "-std=gnu++11")' in compiler_info
