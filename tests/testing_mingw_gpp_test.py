#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


def test_host_compiler_info(testing):
    testing.configure(cpp_compiler_list="i686-w64-mingw32-g++")
    compiler_info = testing.read("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTCXXCompiler.cmake")
    assert 'set(CMAKE_HOSTCXX_COMPILER "/usr/bin/i686-w64-mingw32-g++")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_ID "GNU")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_VERSION "13.0.0")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTCXX_STANDARD_COMPUTED_DEFAULT "17")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_PLATFORM_ID "MinGW")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTCXX_COMPILER_ABI "")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/i686-w64-mingw32/13-win32/include/c++;/usr/lib/gcc/i686-w64-mingw32/13-win32/include/c++/i686-w64-mingw32;/usr/lib/gcc/i686-w64-mingw32/13-win32/include/c++/backward;/usr/lib/gcc/i686-w64-mingw32/13-win32/include;/usr/lib/gcc/i686-w64-mingw32/13-win32/include-fixed;/usr/i686-w64-mingw32/include")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_LIBRARIES "stdc++;mingw32;gcc_s;gcc;moldname;mingwex;kernel32;advapi32;shell32;user32;kernel32;mingw32;gcc_s;gcc;moldname;mingwex;kernel32")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/i686-w64-mingw32/13-win32;/usr/i686-w64-mingw32/lib")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_VERBOSE_FLAG "-v")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_SOURCE_FILE_EXTENSIONS "C;M;c++;cc;cpp;cxx;m;mm;CPP")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_OUTPUT_EXTENSION ".obj")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_EXECUTABLE_SUFFIX ".exe")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_STATIC_LIBRARY_PREFIX "")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_STATIC_LIBRARY_SUFFIX ".lib")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_AR "/usr/bin/i686-w64-mingw32-ar")' in compiler_info
    assert 'set(CMAKE_HOSTCXX_RANLIB "/usr/bin/i686-w64-mingw32-ranlib")' in compiler_info
    assert 'set(CMAKE_INCLUDE_FLAG_HOSTCXX "-I")' in compiler_info
    assert 'set(CMAKE_INCLUDE_SYSTEM_FLAG_HOSTCXX "-isystem ")' in compiler_info
    assert 'set(CMAKE_HOSTCXX11_STANDARD_COMPILE_OPTION "-std=c++11")' in compiler_info
    assert 'set(CMAKE_HOSTCXX11_EXTENSION_COMPILE_OPTION "-std=gnu++11")' in compiler_info
