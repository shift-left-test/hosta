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
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("all").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_test_targets_work(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()
    suffix = '.obj' if c_compiler_list in ["i686-w64-mingw32-gcc"] else '.o'
    assert testing.exists(f"CMakeFiles/HOST-unity_test.dir/calculator/calc.c{suffix}")
    assert testing.exists(f"CMakeFiles/HOST-unity_test.dir/test/unity_test_main.c{suffix}")
    if c_compiler_list not in ["i686-w64-mingw32-gcc"]:
        testing.ctest().check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_link_works(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()
    assert testing.exists("unity_test") or testing.exists("unity_test.exe")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_no_output_interference(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(build="first", cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()
    testing.configure(build="second", cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_ctest_works(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets")
    if c_compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert "unity_test .......................   Passed" in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_gcovr_works(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets")
    if c_compiler_list not in ["clang", "i686-w64-mingw32-gcc"]:
        testing.ctest()
        assert "calculator/calc.c                              8       8   100%" in testing.gcovr().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_no_changes_no_rebuilds(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets")
    assert "Linking HOSTC executable unity_test" not in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_no_configuration_changes_no_rebuilds(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets")
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    assert "Linking HOSTC executable unity_test" not in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_reconfiguration_rebuilds(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DEXTRA_HOSTC_COMPILE_OPTIONS="-g"'])
    testing.cmake("host-targets")
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DEXTRA_HOSTC_COMPILE_OPTIONS=""'])
    assert "Linking HOSTC executable unity_test" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_updating_source_file_rebuilds(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets")
    testing.touch("calculator/calc.c")
    assert "Linking HOSTC executable unity_test" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_updating_header_file_rebuilds(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets")
    testing.touch("calculator/calc.h")
    assert "Linking HOSTC executable unity_test" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_no_standard_option(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    assert '-std=' not in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_standard_option(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DCMAKE_HOSTC_STANDARD=11'])
    assert '-std=gnu11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_invalid_standard_option(testing, cross_toolchain, generator, c_compiler_list):
    stderr = testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DCMAKE_HOSTC_STANDARD=12345']).stderr
    assert "HOSTC_STANDARD is set to invalid value '12345'" in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_standard_and_extension_options(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DCMAKE_HOSTC_STANDARD=11', '-DCMAKE_HOSTC_EXTENSIONS=True'])
    assert '-std=gnu11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_standard_and_no_extension_options(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DCMAKE_HOSTC_STANDARD=11', '-DCMAKE_HOSTC_EXTENSIONS=False'])
    assert '-std=c11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_depends_option(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    assert "hello" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_paths(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    stdout = testing.cmake("host-targets", verbose=True).stdout
    if c_compiler_list in ["i686-w64-mingw32-gcc"]:
        static_library_prefix = ""
        static_library_suffix = ".lib"
        object_extension = ".obj"
    else:
        static_library_prefix = "lib"
        static_library_suffix = ".a"
        object_extension = ".o"

    assert f'-o CMakeFiles/HOST-{static_library_prefix}unity{static_library_suffix}.dir/unity.c{object_extension}' in stdout  # absolute source path
    assert f'{testing.workspace}/external/unity' in stdout  # relative include path to absolute one
    assert testing.exists(f"relative_path_test/CMakeFiles/HOST-relative_path_test.dir/__/calculator/calc.c{object_extension}")  # .. to __

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_compile_options(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DEXTRA_HOSTC_COMPILE_OPTIONS="-g"'])
    assert ' -g' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_link_options(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DEXTRA_HOSTC_LINK_OPTIONS="-lm"'])
    assert ' -lm' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_custom_build_target_conflict_existing_name(testing, cross_toolchain, generator, c_compiler_list):
    stderr = testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=["-DCMAKE_HOST_BUILD_TARGET=all"]).stderr
    assert 'The target name "all" is reserved' in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_custom_build_target(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=["-DCMAKE_HOST_BUILD_TARGET=abc"])
    testing.cmake("abc").check_returncode()
    assert testing.exists("unity_test") or testing.exists("unity_test.exe")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_unity_fixture_add_host_tests_with_unity_fixture_framework(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()
    if c_compiler_list not in ["i686-w64-mingw32-gcc"]:
        stdout = testing.ctest().stdout
        assert 'no_unity_fixture_test' not in stdout
        assert 'FirstGroup.test_plus' in stdout
        assert 'FirstGroup.test_minus' in stdout
        assert 'SecondGroup.test_multiply' in stdout
        assert 'SecondGroup.test_divide' in stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_unity_fixture_add_host_tests_with_ignored_test(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()
    if c_compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert 'FirstGroup.test_minus ............***Not Run (Disabled)' in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_unity_fixture_add_host_tests_with_skipped_test(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("host-targets").check_returncode()
    if c_compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert 'SecondGroup.test_divide ..........   Passed' in testing.ctest().stdout  # Mark unintended tests as passed

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_host_interface_library(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("HOST-coverage").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_host_static_library(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("HOST-unity").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_host_executable(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list)
    testing.cmake("HOST-unity_test").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@pytest.mark.parametrize("c_compiler_list", ["c++", "g++", "clang++", "i686-w64-mingw32-g++"])
def test_with_cpp_compiler(testing, cross_toolchain, generator, c_compiler_list):
    stderr = testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list).stderr
    assert "is not able to compile a simple test program" in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_C_COMPILERS
def test_with_prefix(testing, cross_toolchain, generator, c_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, c_compiler_list=c_compiler_list, extra_options=['-DHOST_TEST_PREFIX="Hello."'])
    testing.cmake("host-targets").check_returncode()
    if c_compiler_list not in ["i686-w64-mingw32-gcc"]:
        stdout = testing.ctest().stdout
        assert 'Hello.unity_test' in stdout
        assert 'Hello.FirstGroup.test_plus' in stdout
        assert 'Hello.FirstGroup.test_minus' in stdout
        assert 'Hello.SecondGroup.test_multiply' in stdout
        assert 'Hello.SecondGroup.test_divide' in stdout
