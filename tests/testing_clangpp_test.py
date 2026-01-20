#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_host_compiler_info(testing):
    testing.configure(cpp_compiler_list="clang++")
    compiler_info = testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTCXXCompiler.cmake")
    assert 'set(CMAKE_HOSTCXX_COMPILER "/usr/bin/clang++")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_ID "Clang")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_VERSION "18.1.3")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTCXX_STANDARD_COMPUTED_DEFAULT "17")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_PLATFORM_ID "Linux")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_INCLUDE_DIRECTORIES "/usr/include/c++/14;/usr/include/x86_64-linux-gnu/c++/14;/usr/include/c++/14/backward;/usr/lib/llvm-18/lib/clang/18/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_LIBRARIES "stdc++;m;gcc_s;gcc;c;gcc_s;gcc")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/14;/usr/lib64;/lib/x86_64-linux-gnu;/lib64;/usr/lib/x86_64-linux-gnu;/lib;/usr/lib")' in compiler_info
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
