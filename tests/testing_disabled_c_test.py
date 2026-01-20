#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

PARAM_CROSS_TOOLCHAIN = pytest.mark.parametrize("cross_toolchain", [True, False])
PARAM_GENERATORS = pytest.mark.parametrize("generator", ["Unix Makefiles", "Ninja"])
PARAM_C_COMPILERS = pytest.mark.parametrize("c_compiler_list", ["cc", "gcc", "clang", "i686-w64-mingw32-gcc"])

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_build_target_works(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list).check_returncode()
    testing.cmake("all").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_build_compiler_info_available(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list).check_returncode()
    assert testing.exists("CMakeFiles/3.28.3/CMakeCCompiler.cmake")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_test_targets_not_available(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()
    assert "No test configuration file found!" in testing.ctest().stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_test_compiler_info_available(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    assert testing.exists("CMakeFiles/3.28.3-hosta.internal/CMakeHOSTCCompiler.cmake")
