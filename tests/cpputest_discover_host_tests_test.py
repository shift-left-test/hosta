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
add_host_library(cpputest STATIC
  SOURCES
    src/CppUTest/CommandLineArguments.cpp
    src/CppUTest/CommandLineTestRunner.cpp
    src/CppUTest/JUnitTestOutput.cpp
    src/CppUTest/MemoryLeakDetector.cpp
    src/CppUTest/MemoryLeakWarningPlugin.cpp
    src/CppUTest/SimpleMutex.cpp
    src/CppUTest/SimpleString.cpp
    src/CppUTest/SimpleStringInternalCache.cpp
    src/CppUTest/TeamCityTestOutput.cpp
    src/CppUTest/TestFailure.cpp
    src/CppUTest/TestFilter.cpp
    src/CppUTest/TestHarness_c.cpp
    src/CppUTest/TestMemoryAllocator.cpp
    src/CppUTest/TestOutput.cpp
    src/CppUTest/TestPlugin.cpp
    src/CppUTest/TestRegistry.cpp
    src/CppUTest/TestResult.cpp
    src/CppUTest/TestTestingFixture.cpp
    src/CppUTest/Utest.cpp
    src/Platforms/Gcc/UtestPlatform.cpp
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_LIST_DIR}
  COMPILE_OPTIONS PUBLIC -DCPPUTEST_MEM_LEAK_DETECTION_DISABLED
)
add_host_executable(unittest
  SOURCES test_file.cpp
  LINK_LIBRARIES PRIVATE Host::cpputest
)
cpputest_discover_host_tests(Host::unittest ${EXTRA_ARGS})
'''

test_file = '''
#include "CppUTest/TestHarness.h"
#include "CppUTest/CommandLineTestRunner.h"
TEST_GROUP(Test) { };
TEST(Test, test) { }
int main(int ac, char** av) {
  return CommandLineTestRunner::RunAllTests(ac, av);
}
'''

def test_prefix_argument(testing):
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="PREFIX;HELLO"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'HELLO' in testing.ctest().stdout

def test_test_list_argument(testing):
    testing.copytree("tests/project/external/cpputest", "")
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
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="DISCOVERY_TIMEOUT;1"']).check_returncode()
    assert 'Process terminated due to timeout' in testing.cmake("host-targets").stderr

def test_extra_args_argument(testing):
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="EXTRA_ARGS;-v"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'Test.test' in testing.ctest('--verbose').stdout

def test_properties_argument(testing):
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal(options=['-DEXTRA_ARGS="PROPERTIES;HELLO;WORLD"']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'HELLO' in testing.read("unittest[1]_tests.cmake")

def test_counter(testing):
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content + "\n" + "cpputest_discover_host_tests(Host::unittest)")
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert testing.exists("unittest[1]_tests.cmake")
    assert testing.exists("unittest[2]_tests.cmake")

def test_blank_file(testing):
    test_file = '''
    int main(int argc, const char* argv[]) {
      return 1;
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    assert 'Error running test executable' in testing.cmake("host-targets").stderr

def test_with_no_tests(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert 'No tests were found' in testing.ctest().stderr

def test_with_no_executable(testing):
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    assert 'unittest_NOT_BUILT' in testing.ctest().stdout

def test_with_passed_tests(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    TEST(Test, test) { }
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................   Passed" in testing.ctest().stdout

def test_with_failed_tests(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    TEST(Test, test) { FAIL("f"); }
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................***Failed" in testing.ctest().stdout

def test_with_disabled_tests(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    IGNORE_TEST(Test, test) { }
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................   Passed" in testing.ctest().stdout  # -ln cannot distinguish IGNORE_TEST, so CppUTest skips it internally and reports pass
