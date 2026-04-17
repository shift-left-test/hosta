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
cpputest_add_host_tests(Host::unittest ${EXTRA_ARGS})
'''

def test_passed(testing):
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

def test_failed(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    TEST(Test, test) { FAIL("forced failure"); }
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

def test_disabled(testing):
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
    assert "Test.test ........................***Not Run (Disabled)" in testing.ctest().stdout

def test_skipped(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    #if 0
    TEST(Test, test) { }
    #endif
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Test.test ........................***Failed" in testing.ctest().stdout  # CppUTest fails when strict filter matches nothing

def test_no_tests(testing):
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
    assert "No tests were found!!!" in testing.ctest().stderr

def test_single_line_commented(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    // TEST(Test, test) { }
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "No tests were found!!!" in testing.ctest().stderr

def test_multi_line_commented(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    /* TEST(Test, test) { } */
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "No tests were found!!!" in testing.ctest().stderr

def test_prefix(testing):
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
    testing.configure_internal(options=['-DEXTRA_ARGS="PREFIX;Hello."']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Hello.Test.test" in testing.ctest().stdout

def test_multiple_test_groups(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(GroupA) { };
    TEST(GroupA, test1) { }
    TEST(GroupA, test2) { }
    TEST_GROUP(GroupB) { };
    TEST(GroupB, test1) { }
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    stdout = testing.ctest().stdout
    assert "GroupA.test1" in stdout
    assert "GroupA.test2" in stdout
    assert "GroupB.test1" in stdout

def test_run_test_multiple_times(testing):
    test_file = '''
    #include "CppUTest/TestHarness.h"
    #include "CppUTest/CommandLineTestRunner.h"
    TEST_GROUP(Test) { };
    TEST(Test, test1) {
    }
    static void runAllTests(void) {
      TEST(Test, test1);
      TEST(Test, test1);
    }
    int main(int ac, char** av) {
      return CommandLineTestRunner::RunAllTests(ac, av);
    }
    '''
    testing.copytree("tests/project/external/cpputest", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.cpp", test_file)
    assert 'test NAME "Test.test1" which already exists' not in testing.configure_internal().stderr
