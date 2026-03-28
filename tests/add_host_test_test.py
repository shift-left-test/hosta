#-*- coding: utf-8 -*-

"""
Copyright (c) 2026 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
project(CMakeTest LANGUAGES NONE)
include(cmake/HostTest.cmake)
enable_testing()
add_host_executable(unittest
  SOURCES test_file.c
)
add_host_test(Host::unittest {extra_args})
'''

def test_passed(testing):
    testing.write("CMakeLists.txt", content.format(extra_args=""))
    testing.write("test_file.c", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "unittest .........................   Passed" in testing.ctest().stdout

def test_failed(testing):
    testing.write("CMakeLists.txt", content.format(extra_args=""))
    testing.write("test_file.c", "int main() { return 1; }")
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "unittest .........................***Failed" in testing.ctest().stdout

def test_prefix(testing):
    testing.write("CMakeLists.txt", content.format(extra_args="PREFIX Hello."))
    testing.write("test_file.c", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Hello.unittest" in testing.ctest().stdout

def test_extra_args(testing):
    test_file = '''
    #include <stdio.h>
    int main(int argc, char* argv[]) {
      for (int i = 0; i < argc; i++) {
        printf("%s\\n", argv[i]);
      }
      return 0;
    }
    '''
    testing.write("CMakeLists.txt", content.format(extra_args="EXTRA_ARGS --hello"))
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "unittest .........................   Passed" in testing.ctest().stdout

def test_testing_disabled(testing):
    cmake = '''
    cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostTest.cmake)
    add_host_executable(unittest SOURCES test_file.c)
    add_host_test(Host::unittest)
    '''
    testing.write("CMakeLists.txt", cmake)
    testing.write("test_file.c", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "No test configuration file found!" in testing.ctest().stderr
