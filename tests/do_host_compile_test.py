#-*- coding: utf-8 -*-

"""
Copyright (c) 2026 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17)
project(CMakeTest LANGUAGES NONE)
enable_testing()
include(cmake/HostTest.cmake)
add_host_executable(main SOURCES main.c COMPILE_OPTIONS PRIVATE -ftest-coverage -fprofile-arcs LINK_OPTIONS PRIVATE -fprofile-arcs)
add_host_test(Host::main)
'''

def test_preserve_gcda_file_when_file_unchanged(testing):
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", "int main(void) { return 0; }")
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()

    testing.ctest().check_returncode()
    assert testing.exists("CMakeFiles/HOST-main.dir/main.c.gcda")

    testing.cmake("host-targets").check_returncode()
    assert testing.exists("CMakeFiles/HOST-main.dir/main.c.gcda")

def test_remove_gcda_file_when_file_changed(testing):
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", "int main(void) { return 0; }")
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()

    testing.ctest().check_returncode()
    assert testing.exists("CMakeFiles/HOST-main.dir/main.c.gcda")

    testing.touch("main.c")
    testing.cmake("host-targets").check_returncode()
    assert not testing.exists("CMakeFiles/HOST-main.dir/main.c.gcda")
