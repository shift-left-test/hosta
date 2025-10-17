#-*- coding: utf-8 -*-

"""
Copyright (c) 2025 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)
project(CMakeTest LANGUAGES NONE)
include(cmake/HostTest.cmake)
enable_testing()
add_host_library(unity_fixture STATIC
  SOURCES unity.c unity_fixture.c
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_LIST_DIR}
  COMPILE_OPTIONS PUBLIC -DUNITY_FIXTURE_NO_EXTRAS
)
add_host_executable(unittest
  SOURCES test_file.c
  LINK_LIBRARIES PRIVATE Host::unity_fixture
)
unity_fixture_discover_host_tests(Host::unittest ${EXTRA_ARGS})
'''

test_file = '''
#include <unity_fixture.h>

TEST_GROUP(Test);
TEST_SETUP(Test) { }
TEST_TEAR_DOWN(Test) { }

TEST(Test, test1) { TEST_ASSERT_TRUE(1); }
TEST(Test, test2) { TEST_ASSERT_TRUE(1); }
TEST(Test, test3) { TEST_ASSERT_TRUE(1); }

static void runAllTests(void) {
  RUN_TEST_CASE(Test, test1);
  RUN_TEST_CASE(Test, test2);
  RUN_TEST_CASE(Test, test3);
}
int main(int argc, const char* argv[]) {
  return UnityMain(argc, argv, runAllTests);
}
'''

def test_prefix_argument(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="PREFIX;HELLO"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'HELLO' in testing.ctest().stdout

def test_test_list_argument(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="TEST_LIST;HELLO"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'HELLO' in testing.read("unittest[1]_tests.cmake")

def test_discovery_timeout_argument(testing):
    test_file = '''
    #include <unistd.h>
    int main(void) {
      sleep(10);
      return 0;
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="DISCOVERY_TIMEOUT;1"']).check_returncode()
    assert 'Process terminated due to timeout' in testing.cmake("host-targets").stderr

def test_extra_args_argument(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="EXTRA_ARGS;-h"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'Display this help message' in testing.ctest('--verbose').stdout

def test_properties_argument(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="PROPERTIES;HELLO;WORLD"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'HELLO' in testing.read("unittest[1]_tests.cmake")

def test_counter(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content + "\n" + "unity_fixture_discover_host_tests(Host::unittest)")
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert testing.exists("unittest[1]_tests.cmake")
    assert testing.exists("unittest[2]_tests.cmake")

def test_blank_file(testing):
    test_file = '''
    int main(int argc, const char* argv[]) {
      return 0;
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    assert 'Error running test executable' in testing.cmake("host-targets").stderr

def test_with_no_tests(testing):
    test_file = '''
    #include <unity_fixture.h>
    static void runAllTests(void) { }
    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'No tests were found' in testing.ctest().stderr

def test_with_no_executable(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    assert 'unittest_NOT_BUILT' in testing.ctest().stdout

def test_with_passed_tests(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    stdout = testing.ctest("--verbose").stdout
    assert 'TEST(Test, test1) PASS' in stdout
    assert 'TEST(Test, test2) PASS' in stdout
    assert 'TEST(Test, test3) PASS' in stdout

def test_with_failed_tests(testing):
    test_file = '''
    #include <unity_fixture.h>

    TEST_GROUP(Test);
    TEST_SETUP(Test) { }
    TEST_TEAR_DOWN(Test) { }

    TEST(Test, test) { TEST_ASSERT_TRUE(0); }

    static void runAllTests(void) {
      RUN_TEST_CASE(Test, test);
    }

    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'Test.test (Failed)' in testing.ctest().stdout

def test_with_ignored_tests(testing):
    test_file = '''
    #include <unity_fixture.h>

    TEST_GROUP(Test);
    TEST_SETUP(Test) { }
    TEST_TEAR_DOWN(Test) { }

    IGNORE_TEST(Test, test) { TEST_ASSERT_TRUE(1); }

    static void runAllTests(void) {
      RUN_TEST_CASE(Test, test);
    }

    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'Not Run (Disabled)' in testing.ctest().stdout

def test_with_commented_tests(testing):
    test_file = '''
    #include <unity_fixture.h>

    TEST_GROUP(Test);
    TEST_SETUP(Test) { }
    TEST_TEAR_DOWN(Test) { }

    TEST(Test, test) { TEST_ASSERT_TRUE(1); }

    static void runAllTests(void) {
    /*
      RUN_TEST_CASE(Test, test);
    */
    }

    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'No tests were found' in testing.ctest().stderr

def test_with_preprocessed_tests(testing):
    test_file = '''
    #include <unity_fixture.h>

    TEST_GROUP(Test);
    TEST_SETUP(Test) { }
    TEST_TEAR_DOWN(Test) { }

    TEST(Test, test) { TEST_ASSERT_TRUE(1); }

    static void runAllTests(void) {
    #if 0
      RUN_TEST_CASE(Test, test);
    #endif
    }

    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'No tests were found' in testing.ctest().stderr
