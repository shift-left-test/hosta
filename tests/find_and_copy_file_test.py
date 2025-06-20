#-*- coding: utf-8 -*-

"""
Copyright (c) 2025 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_unknown_file(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    find_and_copy_file({file} {source_dir} {dest_dir})
    '''
    testing.write("CMakeLists.txt", content.format(file="unknown.file", source_dir="a", dest_dir="b"))
    assert 'Failed to locate unknown.file' in testing.configure_internal().stderr

def test_existing_dest_file(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    find_and_copy_file({file} {source_dir} {dest_dir})
    '''
    testing.mkdirs("build/path/to/dest")
    testing.touch("build/path/to/dest/a.file")
    testing.write("CMakeLists.txt", content.format(file="a.file", source_dir=f"{testing.build}/path/to/source", dest_dir=f"{testing.build}/path/to/dest"))
    assert f"Looking for a.file in {testing.build}/path/to/dest -- found" in testing.configure_internal().stdout

def test_copying_file(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    find_and_copy_file({file} {source_dir} {dest_dir})
    '''
    testing.mkdirs("build/path/to/source")
    testing.touch("build/path/to/source/a.file")
    testing.write("CMakeLists.txt", content.format(file="a.file", source_dir=f"{testing.build}/path/to/source", dest_dir=f"{testing.build}/path/to/dest"))
    testing.configure_internal().check_returncode()
    assert testing.exists(f"path/to/dest/a.file")
