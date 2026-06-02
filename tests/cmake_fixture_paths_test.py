#-*- coding: utf-8 -*-

"""
Copyright (c) 2026 LG Electronics Inc.
SPDX-License-Identifier: MIT

Unit tests for the CMakeFixture version/path helpers (conftest.py).

These guard the helpers that replace the hardcoded CMake version (3.28.3)
previously embedded in 12 test files. The point of the helpers is to derive
the version from the running cmake so the suite keeps working across cmake
upgrades -- so we explicitly prove the helpers are DYNAMIC, not just that they
happen to render the current version.
"""

import re
import subprocess


def _real_cmake_version():
    out = subprocess.run(["cmake", "--version"], capture_output=True, encoding="UTF-8").stdout
    return re.search(r"cmake version (\S+)", out).group(1)


def test_cmake_version_matches_running_cmake(testing):
    # The accessor must report the version of the cmake actually on PATH.
    assert testing.cmake_version == _real_cmake_version()


def test_internal_dir_uses_running_version(testing):
    version = _real_cmake_version()
    assert testing.internal_dir("CMakeHOSTCCompiler.cmake") == \
        f"CMakeFiles/{version}-hosta.internal/CMakeHOSTCCompiler.cmake"


def test_cmake_dir_uses_running_version(testing):
    version = _real_cmake_version()
    assert testing.cmake_dir("CMakeCCompiler.cmake") == \
        f"CMakeFiles/{version}/CMakeCCompiler.cmake"


def test_internal_dir_no_argument_has_no_trailing_slash(testing):
    version = _real_cmake_version()
    assert testing.internal_dir() == f"CMakeFiles/{version}-hosta.internal"


def test_cmake_dir_no_argument_has_no_trailing_slash(testing):
    version = _real_cmake_version()
    assert testing.cmake_dir() == f"CMakeFiles/{version}"


def test_helpers_are_dynamic_not_hardcoded(testing):
    # Inject a fake version and confirm the paths follow it. This is what proves
    # the helpers won't silently break when CI bumps cmake: if they were
    # hardcoded to 3.28.3, these assertions would fail.
    testing.cmake_version = "9.99.0"
    assert testing.internal_dir("X") == "CMakeFiles/9.99.0-hosta.internal/X"
    assert testing.cmake_dir("X") == "CMakeFiles/9.99.0/X"
    assert "3.28.3" not in testing.internal_dir("X")
