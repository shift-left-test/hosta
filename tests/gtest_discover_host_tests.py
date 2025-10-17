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
gtest_discover_host_tests(Host::unittest ${EXTRA_ARGS})
'''

test_file = '''
#include <gtest/gtest.h>
TEST(Test, test) { SUCCEED(); }
int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
'''

def test_prefix_argument(testing):
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="PREFIX;HELLO"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'HELLO' in testing.ctest().stdout

def test_test_list_argument(testing):
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
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
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="DISCOVERY_TIMEOUT;1"']).check_returncode()
    assert 'Process terminated due to timeout' in testing.cmake("host-targets").stderr

def test_extra_args_argument(testing):
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="EXTRA_ARGS;-h"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'Google Test' in testing.ctest('--verbose').stdout

def test_properties_argument(testing):
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="PROPERTIES;HELLO;WORLD"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'HELLO' in testing.read("unittest[1]_tests.cmake")

def test_counter(testing):
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content + "\n" + "gtest_discover_host_tests(Host::unittest)")
    testing.write("test_file.cpp", test_file)
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
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'No tests were found' in testing.ctest().stderr

def test_with_no_tests(testing):
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
    assert 'No tests were found' in testing.ctest().stderr

def test_with_no_executable(testing):
    testing.copytree("tests/project/external/gtest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    assert 'unittest_NOT_BUILT' in testing.ctest().stdout

def test_with_passed_tests(testing):
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

def test_with_failed_tests(testing):
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

def test_with_disabled_tests(testing):
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

def test_with_commented_tests(testing):
    test_file = '''
    #include <gtest/gtest.h>
    /*
    TEST(Test, test) { SUCCEED(); }
    */
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
    assert 'No tests were found' in testing.ctest().stderr

def test_with_preprocessed_tests(testing):
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
    assert 'No tests were found' in testing.ctest().stderr

def test_with_fixture(testing):
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

def test_with_parameterized(testing):
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
    assert "SimpleValues/AddTest.add/(1,2) ...   Passed" in testing.ctest().stdout
