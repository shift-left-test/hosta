#-*- coding: utf-8 -*-

"""
Copyright (c) 2025 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
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
option(ENABLE_HOST_UNITY_FIXTURE_EXACT_MATCH "Unity fixture exact matching" OFF)
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
    assert "UnitTest.test ....................   Passed" in testing.ctest().stdout

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
    assert "UnitTest.test ....................***Failed" in testing.ctest().stdout

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
    assert "UnitTest.test ....................***Not Run (Disabled)" in testing.ctest().stdout

def test_ignored_at_runtime(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_IGNORE_MESSAGE("conditionally skipped");
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
    assert "UnitTest.test ....................***Skipped" in testing.ctest().stdout

def test_skip_does_not_mask_failure_in_substring_mode(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) { TEST_FAIL_MESSAGE("boom"); }
    IGNORE_TEST(UnitTest, test_ignored) { }
    static void runAllTests(void) {
      RUN_TEST_CASE(UnitTest, test);
      RUN_TEST_CASE(UnitTest, test_ignored);
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
    out = testing.ctest().stdout
    # Default substring mode: "-n test" also selects "test_ignored", so the entry
    # runs both -> "2 Tests 1 Failures 1 Ignored"; the failure must not be masked.
    assert "***Failed" in out
    assert "UnitTest.test ....................***Skipped" not in out

def test_skip_does_not_mask_ten_failures(testing):
    # "c" is a substring of every case, so "Group.c" runs all ten failures plus
    # the ignored one -> "11 Tests 10 Failures 1 Ignored"; the "0 Failures" inside
    # "10 Failures" must not trigger a skip.
    fails = "".join(
        'TEST(Group, c%s) { TEST_FAIL_MESSAGE("boom"); }\n    ' % s
        for s in [""] + [str(i) for i in range(9)]
    )
    runs = "".join(
        'RUN_TEST_CASE(Group, c%s);\n      ' % s
        for s in [""] + [str(i) for i in range(9)]
    )
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(Group);
    TEST_SETUP(Group) { }
    TEST_TEAR_DOWN(Group) { }
    %sIGNORE_TEST(Group, c_ignored) { }
    static void runAllTests(void) {
      %sRUN_TEST_CASE(Group, c_ignored);
    }
    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    ''' % (fails, runs)
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    out = testing.ctest().stdout
    # Inspect the "Group.c" entry only (not Group.c0..c8 / Group.c_ignored).
    import re
    gc_lines = [l for l in out.splitlines() if re.search(r'Group\.c(?![0-9_])', l)]
    assert gc_lines, "Group.c entry not found in:\n" + out
    assert not any("Skipped" in l for l in gc_lines), \
        "10 failures masked as Skipped:\n" + "\n".join(gc_lines)

def test_preprocessor_excluded_tests_do_not_misfire_skip(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, active) { TEST_ASSERT_TRUE(1); }
    #if 0
    IGNORE_TEST(UnitTest, excluded_ignore) { }
    TEST(UnitTest, excluded_runtime) { TEST_IGNORE(); }
    #endif
    static void runAllTests(void) {
      RUN_TEST_CASE(UnitTest, active);
    #if 0
      RUN_TEST_CASE(UnitTest, excluded_ignore);
      RUN_TEST_CASE(UnitTest, excluded_runtime);
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
    out = testing.ctest().stdout
    # add mode scans raw source (no preprocessor), so #if 0 code is still
    # registered as ghost tests; the skip regex must not misfire on them.
    assert "UnitTest.active" in out
    assert "***Skipped" not in out

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
    assert "UnitTest.test ....................   Passed" in testing.ctest().stdout  # Mark unintended tests as passed

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
    assert "UnitTest.test ....................   Passed" in testing.ctest().stdout  # Mark unintended tests as passed

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
    assert "No tests were found!!!" in testing.ctest().stderr

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
    assert "No tests were found!!!" in testing.ctest().stderr

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
    assert "No tests were found!!!" in testing.ctest().stderr

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
    assert "UnitTest.test ....................   Passed" in testing.ctest().stdout

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
    assert 'test NAME "UnitTest.test" which already exists' not in testing.configure_internal().stderr

test_file = '''
#include <unity_fixture.h>

TEST_GROUP(Test1);
TEST_SETUP(Test1) { }
TEST_TEAR_DOWN(Test1) { }
TEST(Test1, test1) { TEST_ASSERT_TRUE(1); }

TEST_GROUP(Test123);
TEST_SETUP(Test123) { }
TEST_TEAR_DOWN(Test123) { }
TEST(Test123, test123) { TEST_ASSERT_TRUE(1); }

static void runAllTests(void) {
  RUN_TEST_CASE(Test1, test1);
  RUN_TEST_CASE(Test123, test123);
}

int main(int argc, const char* argv[]) {
  return UnityMain(argc, argv, runAllTests);
}
'''

def test_prefix(testing):
    content_with_prefix = '''
    cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
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
    unity_fixture_add_host_tests(Host::unittest PREFIX Hello.)
    '''
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
    testing.write("CMakeLists.txt", content_with_prefix)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "Hello.UnitTest.test" in testing.ctest().stdout

def test_properties(testing):
    content_with_properties = '''
    cmake_minimum_required(VERSION 3.17 FATAL_ERROR)
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
    unity_fixture_add_host_tests(Host::unittest
      PROPERTIES ENVIRONMENT "HOSTA_TEST_ENV=hello"
    )
    '''
    test_file = '''
    #include <unity_fixture.h>
    #include <stdlib.h>
    TEST_GROUP(UnitTest);
    TEST_SETUP(UnitTest) { }
    TEST_TEAR_DOWN(UnitTest) { }
    TEST(UnitTest, test) {
      TEST_ASSERT_EQUAL_STRING("hello", getenv("HOSTA_TEST_ENV"));
    }
    static void runAllTests(void) {
      RUN_TEST_CASE(UnitTest, test);
    }
    int main(int argc, const char* argv[]) {
      return UnityMain(argc, argv, runAllTests);
    }
    '''
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content_with_properties)
    testing.write("test_file.c", test_file)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()
    assert "UnitTest.test ....................   Passed" in testing.ctest().stdout

def test_multiple_test_groups(testing):
    test_file = '''
    #include <unity_fixture.h>
    TEST_GROUP(GroupA);
    TEST_SETUP(GroupA) { }
    TEST_TEAR_DOWN(GroupA) { }
    TEST(GroupA, test1) { TEST_ASSERT_TRUE(1); }
    TEST(GroupA, test2) { TEST_ASSERT_TRUE(1); }

    TEST_GROUP(GroupB);
    TEST_SETUP(GroupB) { }
    TEST_TEAR_DOWN(GroupB) { }
    TEST(GroupB, test1) { TEST_ASSERT_TRUE(1); }

    static void runAllTests(void) {
      RUN_TEST_CASE(GroupA, test1);
      RUN_TEST_CASE(GroupA, test2);
      RUN_TEST_CASE(GroupB, test1);
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
    assert "GroupA.test1" in stdout
    assert "GroupA.test2" in stdout
    assert "GroupB.test1" in stdout

def test_enable_exact_match_with_unknown_group_name(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DENABLE_HOST_UNITY_FIXTURE_EXACT_MATCH=ON']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    stderr = testing.ctest('-R Test\\.test --verbose').stderr
    assert 'No tests were found!!!' in stderr

def test_enable_exact_match_with_known_group_name(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DENABLE_HOST_UNITY_FIXTURE_EXACT_MATCH=ON']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    stdout = testing.ctest('-R Test1\\.test --verbose').stdout
    assert 'TEST(Test1, test1) PASS' in stdout
    assert 'TEST(Test123, test123) PASS' not in stdout

def test_enable_exact_match_with_unknown_test_name(testing):
    testing.copytree("tests/project/external/unity", "")
    testing.write("CMakeLists.txt", content)
    testing.write("test_file.c", test_file)
    testing.configure_internal(options=['-DENABLE_HOST_UNITY_FIXTURE_EXACT_MATCH=ON']).check_returncode()
    testing.cmake("host-targets").check_returncode()
    stdout = testing.ctest('-R Test1\\.test1 --verbose').stdout
    assert 'TEST(Test1, test1) PASS' in stdout
    assert 'TEST(Test123, test123) PASS' not in stdout
