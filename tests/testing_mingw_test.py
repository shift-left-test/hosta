#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_build_target_works(testing_mingw):
    testing_mingw.cmake("all").check_returncode()

def test_build_test_target_works(testing_mingw):
    testing_mingw.cmake("build-test").check_returncode()

def test_compile_works(testing_mingw):
    testing_mingw.cmake("build-test").check_returncode()
    assert testing_mingw.exists("sample/CMakeFiles/unittest.dir/src/calc.c.o")
    assert testing_mingw.exists("sample/CMakeFiles/unittest.dir/test/test_main.c.o")

def test_link_works(testing_mingw):
    testing_mingw.cmake("build-test").check_returncode()
    assert testing_mingw.exists("sample/unittest.out")

def test_no_output_interference(testing_mingw):
    testing_mingw.prepare("")
    testing_mingw.cmake("build-test").check_returncode()
    testing_mingw.prepare("temp")
    testing_mingw.cmake("build-test").check_returncode()

def test_host_compiler_info(testing_mingw):
    compiler_info = testing_mingw.read("CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/i686-w64-mingw32-gcc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/i686-w64-mingw32/9.3-win32/include;/usr/lib/gcc/i686-w64-mingw32/9.3-win32/include-fixed;/usr/i686-w64-mingw32/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "mingw32;gcc;moldname;mingwex;advapi32;shell32;user32;kernel32;mingw32;gcc;moldname;mingwex")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/i686-w64-mingw32/9.3-win32;/usr/i686-w64-mingw32/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
