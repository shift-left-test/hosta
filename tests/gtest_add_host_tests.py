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
add_host_library(googletest STATIC
  SOURCES gtest-all.cc
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_LIST_DIR}
  COMPILE_OPTIONS PUBLIC -DGTEST_HAS_PTHREAD=0
)
add_host_executable(unittest
  SOURCES test_file.cpp
  LINK_LIBRARIES PRIVATE Host::googletest
)
gtest_add_host_tests(Host::unittest)
'''

def test_passed(testing):
    test_file = '''
    #include <gtest/gtest.h>
    TEST(Test, test) { SUCCEED(); }
    int main(int argc, char* argv[]) {
      ::testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................   Passed" in testing.ctest().stdout

def test_failed(testing):
    test_file = '''
    #include <gtest/gtest.h>
    TEST(Test, test) { FAIL(); }
    int main(int argc, char* argv[]) {
      ::testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................***Failed" in testing.ctest().stdout

def test_disabled(testing):
    test_file = '''
    #include <gtest/gtest.h>
    TEST(Test, DISABLED_test) { SUCCEED(); }
    int main(int argc, char* argv[]) {
      ::testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................***Not Run (Disabled)" in testing.ctest().stdout

def test_skipped(testing):
    test_file = '''
    #include <gtest/gtest.h>
    #if 0
    TEST(Test, test) { SUCCEED(); }
    #endif
    int main(int argc, char* argv[]) {
      ::testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................   Passed" in testing.ctest().stdout  # gtest marks unexecuted tests as passed

def test_no_tests(testing):
    test_file = '''
    #include <gtest/gtest.h>
    int main(int argc, char* argv[]) {
      ::testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "No tests were found!!!" in testing.ctest().stderr

def test_no_test_framework(testing):
    test_file = '''
    #include <gtest/gtest.h>
    int main(int argc, char* argv[]) {
      return 0;
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "No tests were found!!!" in testing.ctest().stderr

def test_fixture_works(testing):
    test_file = '''
    #include <gtest/gtest.h>
    class Test : public ::testing::Test {
     protected:
      void SetUp() override { }
      void TearDown() override { }
    };
    TEST_F(Test, test) { SUCCEED(); }
    int main(int argc, char* argv[]) {
      ::testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................   Passed" in testing.ctest().stdout

def test_parameterized_works(testing):
    test_file = '''
    #include <utility>
    #include <gtest/gtest.h>

    inline int add(int a, int b) { return a + b; }

    class AddTest : public ::testing::TestWithParam<std::pair<int, int>> { };

    TEST_P(AddTest, add) {
      auto param = GetParam();
      int a = param.first;
      int b = param.second;
      EXPECT_EQ(a + b, add(a, b));
    }

    INSTANTIATE_TEST_SUITE_P(
      SimpleValues,
      AddTest,
      ::testing::Values(std::make_pair(1, 2), std::make_pair(3, 4))
    );

    int main(int argc, char* argv[]) {
      ::testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }
    '''
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "*/AddTest.add/* ..................   Passed" in testing.ctest().stdout
