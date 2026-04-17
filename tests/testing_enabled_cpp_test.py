#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

PARAM_CROSS_TOOLCHAIN = pytest.mark.parametrize("cross_toolchain", [True, False])
PARAM_GENERATORS = pytest.mark.parametrize("generator", ["Unix Makefiles", "Ninja"])
PARAM_CPP_COMPILERS = pytest.mark.parametrize("cpp_compiler_list", ["c++", "g++", "clang++", "i686-w64-mingw32-g++"])

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_build_target_works(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("all").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_test_targets_work(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()
    suffix = '.obj' if cpp_compiler_list in ["i686-w64-mingw32-g++"] else '.o'
    assert testing.exists(f"test/CMakeFiles/HOST-google_test.dir/__/calculator/calc.cpp{suffix}")
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        testing.ctest().check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_link_works(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()
    assert testing.exists("test/google_test") or testing.exists("test/google_test.exe")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_no_output_interference(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(build="first", cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()
    testing.configure(build="second", cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_ctest_works(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets")
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        assert "GoogleTest.test_plus .............   Passed" in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_gcovr_works(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets")
    if cpp_compiler_list not in ["clang++", "i686-w64-mingw32-g++"]:
        testing.ctest()
        assert "calculator/calc.cpp                            8       6    75%" in testing.gcovr().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_no_changes_no_rebuilds(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets")
    assert "Linking HOSTCXX executable google_test" not in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_no_configuration_changes_no_rebuilds(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets")
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    assert "Linking HOSTCXX executable google_test" not in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_reconfiguration_rebuilds(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DEXTRA_HOSTCXX_COMPILE_OPTIONS="-g"'])
    testing.cmake("host-targets")
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DEXTRA_HOSTCXX_COMPILE_OPTIONS=""'])
    assert "Linking HOSTCXX executable google_test" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_updating_source_file_rebuilds(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets")
    testing.touch("calculator/calc.cpp")
    assert "Linking HOSTCXX executable google_test" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_updating_header_file_rebuilds(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets")
    testing.touch("calculator/calc.hpp")
    assert "Linking HOSTCXX executable google_test" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_no_standard_option(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    assert '-std=' not in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_standard_option(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DCMAKE_HOSTCXX_STANDARD=11'])
    assert '-std=gnu++11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_invalid_standard_option(testing, cross_toolchain, generator, cpp_compiler_list):
    stderr = testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DCMAKE_HOSTCXX_STANDARD=12345']).stderr
    assert "HOSTCXX_STANDARD is set to invalid value '12345'" in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_standard_and_extension_options(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DCMAKE_HOSTCXX_STANDARD=11', '-DCMAKE_HOSTCXX_EXTENSIONS=True'])
    assert '-std=gnu++11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_standard_and_no_extension_options(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DCMAKE_HOSTCXX_STANDARD=11', '-DCMAKE_HOSTCXX_EXTENSIONS=False'])
    assert '-std=c++11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_depends_option(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    assert "hello" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_paths(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    stdout = testing.cmake("host-targets", verbose=True).stdout
    if cpp_compiler_list in ["i686-w64-mingw32-g++"]:
        static_library_prefix = ""
        static_library_suffix = ".lib"
        object_extension = ".obj"
    else:
        static_library_prefix = "lib"
        static_library_suffix = ".a"
        object_extension = ".o"
    assert f'-o CMakeFiles/HOST-{static_library_prefix}gtest{static_library_suffix}.dir/gtest-all.cc{object_extension}' in stdout  # absolute source path
    assert f'{testing.workspace}/external/gtest' in stdout  # relative include path to absolute one

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_compile_options(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DEXTRA_HOSTCXX_COMPILE_OPTIONS="-g"'])
    assert ' -g' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_link_options(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DEXTRA_HOSTCXX_LINK_OPTIONS="-lm"'])
    assert ' -lm' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_custom_build_target_conflict_existing_name(testing, cross_toolchain, generator, cpp_compiler_list):
    stderr = testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=["-DCMAKE_HOST_BUILD_TARGET=all"]).stderr
    assert 'The target name "all" is reserved' in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_custom_build_target(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=["-DCMAKE_HOST_BUILD_TARGET=abc"])
    testing.cmake("abc").check_returncode()
    assert testing.exists("test/google_test") or testing.exists("test/google_test.exe")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_gtest_add_host_tests_with_googletest_framework(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        stdout = testing.ctest().stdout
        assert 'GoogleTest.test_plus' in stdout
        assert 'GoogleTest.test_minus' in stdout
        assert 'GoogleTest.test_multiply' in stdout
        assert 'GoogleTest.test_divide' in stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_gtest_add_host_tests_with_ignored_test(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        assert 'GoogleTest.test_minus ............***Not Run (Disabled)' in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_host_interface_library(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("HOST-coverage").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_host_static_library(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("HOST-gtest").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_host_executable(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("HOST-google_test").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@pytest.mark.parametrize("cpp_compiler_list", ["cc", "gcc", "clang", "i686-w64-mingw32-gcc"])
def test_with_c_compiler(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list).check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_with_prefix(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DHOST_TEST_PREFIX="Hello."'])
    testing.cmake("host-targets").check_returncode()
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        stdout = testing.ctest().stdout
        assert "Hello.GoogleTest.test_plus" in stdout
        assert "Hello.GoogleTest.test_minus" in stdout
        assert "Hello.GoogleTest.test_multiply" in stdout
        assert "Hello.GoogleTest.test_divide" in stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_cpputest_add_host_tests(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        stdout = testing.ctest().stdout
        assert 'CppUTestCalc.test_plus' in stdout
        assert 'CppUTestCalc.test_multiply' in stdout
        assert 'CppUTestCalc.test_divide' in stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_cpputest_add_host_tests_with_ignored_test(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list)
    testing.cmake("host-targets").check_returncode()
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        assert 'CppUTestCalc.test_minus .........' in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_CPP_COMPILERS
def test_cpputest_add_host_tests_with_prefix(testing, cross_toolchain, generator, cpp_compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, cpp_compiler_list=cpp_compiler_list, extra_options=['-DHOST_TEST_PREFIX="Hello."'])
    testing.cmake("host-targets").check_returncode()
    if cpp_compiler_list not in ["i686-w64-mingw32-g++"]:
        stdout = testing.ctest().stdout
        assert "Hello.CppUTestCalc.test_plus" in stdout
        assert "Hello.CppUTestCalc.test_multiply" in stdout
        assert "Hello.CppUTestCalc.test_divide" in stdout
