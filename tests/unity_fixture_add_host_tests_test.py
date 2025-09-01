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
unity_fixture_add_host_tests(Host::unittest)
'''

def test_passed(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    static void runAllTests(void) {
      RUN_TEST_CASE(UnitTest, test);
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
    stdout = testing.ctest().stdout
    assert "UnitTest.test ....................   Passed" in stdout

def test_failed(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_FAIL();
    }
    static void runAllTests(void) {
      RUN_TEST_CASE(UnitTest, test);
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
    stdout = testing.ctest().stdout
    assert "UnitTest.test ....................***Failed" in stdout

def test_disabled(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    IGNORE_TEST(UnitTest, test) {
      TEST_FAIL();
    }
    static void runAllTests(void) {
      RUN_TEST_CASE(UnitTest, test);
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
    stdout = testing.ctest().stdout
    assert "UnitTest.test ....................***Not Run (Disabled)" in stdout

def test_skipped(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    static void runAllTests(void) {
    #if 0
      RUN_TEST_CASE(UnitTest, test);
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
    stdout = testing.ctest().stdout
    assert "UnitTest.test ....................***Skipped" in stdout

def test_skipped_no_tests(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    #if 0
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    #endif
    static void runAllTests(void) {
    #if 0
      RUN_TEST_CASE(UnitTest, test);
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
    stdout = testing.ctest().stdout
    assert "UnitTest.test ....................***Skipped" in stdout

def test_no_tests(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    static void runAllTests(void) {
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
    stderr = testing.ctest().stderr
    assert "No tests were found!!!" in stderr

def test_single_line_commented(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    static void runAllTests(void) {
      // RUN_TEST_CASE(UnitTest, test);
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
    stderr = testing.ctest().stderr
    assert "No tests were found!!!" in stderr

def test_multi_line_commented(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    static void runAllTests(void) {
    /*
      RUN_TEST_CASE(UnitTest, test);
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
    stderr = testing.ctest().stderr
    assert "No tests were found!!!" in stderr

def test_passed_with_multi_line_comments(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    static void runAllTests(void) {
    /*
      RUN_TEST_CASE(UnitTest, test);
    */
      RUN_TEST_CASE(UnitTest, test);
    /*
      RUN_TEST_CASE(UnitTest, test);
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
    stdout = testing.ctest().stdout
    assert "UnitTest.test ....................   Passed" in stdout

def test_run_test_case_multiple_times(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_TRUE(1);
    }
    static void runAllTests(void) {
      RUN_TEST_CASE(UnitTest, test);
      RUN_TEST_CASE(UnitTest, test);
    }
    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    stderr = testing.configure_internal().stderr
    assert 'test NAME "UnitTest.test" which already exists' not in stderr
