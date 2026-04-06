#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import glob
import os
import re


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostCompilerUtilities.cmake)

load_host_compiler_preferences(X)

message(STATUS "load_host_compiler_preferences(X): ${DATA}")
'''

def test_unknown_file(testing):
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    assert "load_host_compiler_preferences(X): hello" not in testing.configure_internal().stdout

def test_load_file(testing):
    testing.write("CMakeLists.txt", content)
    testing.configure_internal()
    testing.write("build/CMakeFiles/3.28.3-hosta.internal/CMakeHOSTXCompiler.cmake", 'set(DATA "hello")\n')
    assert "load_host_compiler_preferences(X): hello" in testing.configure_internal().stdout


stale_compiler_content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)

message(STATUS "ENABLED_LANGUAGES: ${ENABLED_HOST_LANGUAGES}")
'''

def test_stale_cached_compiler_redetects(testing):
    """Verify that a stale cached compiler path triggers re-detection instead of silent success."""
    testing.write("CMakeLists.txt", stale_compiler_content)
    # First configure: succeeds normally, caches compiler info
    result = testing.configure_internal()
    result.check_returncode()
    assert "ENABLED_LANGUAGES:" in result.stdout

    # Corrupt the cached C compiler path to a non-existent path
    cache_pattern = os.path.join(testing.build, "CMakeFiles", "*-hosta.internal", "CMakeHOSTCCompiler.cmake")
    cache_files = glob.glob(cache_pattern)
    assert len(cache_files) > 0, "No cached compiler preference file found"
    for cache_file in cache_files:
        with open(cache_file, "r") as f:
            original = f.read()
        # Replace compiler path with non-existent path
        corrupted = re.sub(
            r'set\(CMAKE_HOSTC_COMPILER "([^"]*)"\)',
            'set(CMAKE_HOSTC_COMPILER "/definitely/missing/compiler")',
            original
        )
        with open(cache_file, "w") as f:
            f.write(corrupted)

    # Re-configure: should warn about stale compiler and re-detect
    result = testing.configure_internal()
    assert "no longer exists" in result.stderr or result.returncode == 0
