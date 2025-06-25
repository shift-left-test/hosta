#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_existing_target(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES main.c)
    add_host_executable(hello SOURCES main.c)
    '''
    testing.write("main.c", "int main() { return 0; }")
    testing.write("CMakeLists.txt", content)
    assert 'add_custom_target cannot create target "HOST-hello"' in testing.configure_internal().stderr

def test_host_namespace_target(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(Host::hello SOURCES main.c)
    '''
    testing.write("main.c", "int main() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert 'Linking HOSTC executable hello' in testing.cmake("host-targets", verbose=True).stdout

def test_no_source(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello)
    '''
    testing.write("CMakeLists.txt", content)
    assert 'No SOURCES given to target: hello' in testing.configure_internal().stderr

def test_unknown_source(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES unknown.c)
    '''
    testing.write("CMakeLists.txt", content)
    assert 'Cannot find source file:\n\n    unknown.c' in testing.configure_internal().stderr

def test_sources(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES main.c hello.c)
    '''
    testing.write("hello.c", "void hello() { }")
    testing.write("main.c", "#include <stdio.h> \n int main() { hello(); return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()

def test_include_directories(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES main.c INCLUDE_DIRECTORIES PRIVATE first second)
    '''
    testing.write("main.c", "int main() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert f'-I{testing.workspace}/first -I{testing.workspace}/second' in testing.cmake("host-targets", verbose=True).stdout

def test_compile_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES main.c COMPILE_OPTIONS PRIVATE -DHELLO -DWORLD)
    '''
    testing.write("main.c", "#ifdef HELLO void hello() { } \n #endif \n #ifdef WORLD \n int main() { return 0; } \n #endif")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()

def test_link_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES main.c LINK_OPTIONS PRIVATE -fprofile-arcs -lm)
    '''
    testing.write("main.c", "int main() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert '-fprofile-arcs -lm' in testing.cmake("host-targets", verbose=True).stdout

def test_link_static_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello Host::world)
    add_host_library(hello STATIC SOURCES hello/hello.c INCLUDE_DIRECTORIES PUBLIC hello COMPILE_OPTIONS PUBLIC -DHELLO LINK_OPTIONS PUBLIC -fprofile-arcs)
    add_host_library(world STATIC SOURCES world/world.c INCLUDE_DIRECTORIES PUBLIC world COMPILE_OPTIONS PUBLIC -DWORLD LINK_OPTIONS PUBLIC -lm)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", '#include "hello.h" \n #include "world.h" \n int main() { hello(); world(); return 0; }')
    testing.write("hello/hello.h", "void hello();")
    testing.write("hello/hello.c", "void hello() { }")
    testing.write("world/world.h", "void world();")
    testing.write("world/world.c", "void world() { }")

    testing.configure_internal().check_returncode()
    process = testing.cmake("host-targets", verbose=True)
    process.check_returncode()
    stdout = process.stdout
    assert f'-I{testing.workspace}/hello -I{testing.workspace}/world' in stdout
    assert '-DHELLO -DWORLD' in stdout
    assert f'-fprofile-arcs {testing.build}/libhello.a -lm' in stdout

def test_link_interface_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello Host::world)
    add_host_library(hello INTERFACE INCLUDE_DIRECTORIES PUBLIC hello COMPILE_OPTIONS PUBLIC -DHELLO LINK_OPTIONS PUBLIC -fprofile-arcs)
    add_host_library(world INTERFACE INCLUDE_DIRECTORIES PUBLIC world COMPILE_OPTIONS PUBLIC -DWORLD LINK_OPTIONS PUBLIC -lm)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", 'int main() { return 0; }')
    testing.configure_internal().check_returncode()
    process = testing.cmake("host-targets", verbose=True)
    process.check_returncode()
    stdout = process.stdout
    assert f'-I{testing.workspace}/hello -I{testing.workspace}/world' in stdout
    assert '-DHELLO -DWORLD' in stdout
    assert '-fprofile-arcs -lm' in stdout

def test_link_libraries_with_private_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello)
    add_host_library(hello INTERFACE INCLUDE_DIRECTORIES PRIVATE aaa COMPILE_OPTIONS PRIVATE bbb LINK_OPTIONS PRIVATE ccc)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    process = testing.cmake("host-targets", verbose=True)
    process.check_returncode()
    stdout = process.stdout
    assert '-I' not in stdout
    assert 'aaa' not in stdout
    assert 'bbb' not in stdout
    assert 'ccc' not in stdout

def test_executable_rebuild(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    assert 'Scanning dependencies of target HOST-main' in testing.cmake("host-targets").stdout
    assert not 'Scanning dependencies of target HOST-main' in testing.cmake("host-targets").stdout

def test_include_before_project(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    include(cmake/HostBuild.cmake)
    project(CMakeTest LANGUAGES NONE)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello Host::world)
    add_host_library(hello INTERFACE INCLUDE_DIRECTORIES PUBLIC hello COMPILE_OPTIONS PUBLIC -DHELLO LINK_OPTIONS PUBLIC -fprofile-arcs)
    add_host_library(world INTERFACE INCLUDE_DIRECTORIES PUBLIC world COMPILE_OPTIONS PUBLIC -DWORLD LINK_OPTIONS PUBLIC -lm)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", 'int main() { return 0; }')
    testing.configure_internal().check_returncode()
    process = testing.cmake("host-targets", verbose=True)
    process.check_returncode()
    stdout = process.stdout
    assert f'-I{testing.workspace}/hello -I{testing.workspace}/world' in stdout
    assert '-DHELLO -DWORLD' in stdout
    assert '-fprofile-arcs -lm' in stdout

def test_generator_expression_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c COMPILE_OPTIONS PRIVATE $<TARGET_PROPERTY:HOST-hello,HOST_INTERFACE_COMPILE_OPTIONS>)
    add_host_library(hello INTERFACE COMPILE_OPTIONS PUBLIC -DHELLO)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", '#ifdef HELLO \n int main() { return 0; } \n #endif')
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets", verbose=True).check_returncode()

def test_with_unknown_host_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE Host::unknown)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", 'int main() { return 0; }')
    assert 'Error evaluating generator expression' in testing.configure_internal().stderr

def test_with_normal_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE hello)
    add_library(hello STATIC hello/hello.c)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", '#include "hello.h" \n int main() { hello(); return 0; }')
    testing.write("hello/hello.h", "void hello();")
    testing.write("hello/hello.c", "void hello() { }")
    assert 'Unsupported libraries: hello' in testing.configure_internal().stderr

def test_with_unknown_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE hello world)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", 'int main() { return 0; }')
    assert 'Unsupported libraries: hello, world' in testing.configure_internal().stderr

def test_with_host_executable_as_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(main SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello)
    add_host_executable(hello SOURCES hello/hello.c)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("main.c", "int main() { return 0; }")
    testing.write("hello/hello.c", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    testing.cmake("HOST-hello").check_returncode()
    assert not 'libhello.a' in testing.cmake("HOST-main", verbose=True).stdout

def test_replace_special_characters_in_path(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES "{filename}")
    '''
    testing.write("CMakeLists.txt", content.format(filename='\\":*?<>| .c'))
    testing.write('":*?<>| .c', "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    assert 'CMakeFiles/HOST-hello.dir/________.c.o' in testing.cmake("host-targets", verbose=True).stdout

def test_cmake_host_flags(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)

    set(CMAKE_HOSTC_FLAGS "-DHOSTC_FLAGS_1;-DHOSTC_FLAGS_2")
    set(CMAKE_HOSTCXX_FLAGS "-DHOSTCXX_FLAGS_1;-DHOSTCXX_FLAGS_2")

    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES "{c_file}" "{cxx_file}")
    '''
    testing.write("CMakeLists.txt", content.format(c_file="c.c", cxx_file="cxx.cc"))
    testing.write("c.c", "int main() { return 0; }")
    testing.write("cxx.cc", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("host-targets", verbose=True).stdout
    assert '-DHOSTC_FLAGS_1 -DHOSTC_FLAGS_2' in stdout
    assert '-DHOSTCXX_FLAGS_1 -DHOSTCXX_FLAGS_2' in stdout

def test_cmake_host_exe_linker_flags(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)

    set(CMAKE_HOST_EXE_LINKER_FLAGS "-fno-common -fno-builtin")

    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES "{c_file}" "{cxx_file}")
    '''
    testing.write("CMakeLists.txt", content.format(c_file="c.c", cxx_file="cxx.cc"))
    testing.write("c.c", "int main() { return 0; }")
    testing.write("cxx.cc", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("host-targets", verbose=True).stdout
    assert '-fno-common -fno-builtin' in stdout

def test_cmake_host_include_path(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)

    set(CMAKE_HOST_INCLUDE_PATH "/include/first;/include/second")

    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES "{c_file}" "{cxx_file}")
    '''
    testing.write("CMakeLists.txt", content.format(c_file="c.c", cxx_file="cxx.cc"))
    testing.write("c.c", "int main() { return 0; }")
    testing.write("cxx.cc", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("host-targets", verbose=True).stdout
    assert '-I/include/first -I/include/second' in stdout

def test_execlude_from_all_target(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES "hello.c" EXCLUDE_FROM_ALL)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("hello.c", "int main() { return 0; }")
    testing.configure_internal().check_returncode()
    assert 'Nothing to be done' in testing.cmake("host-targets", verbose=True).stdout

def test_build_excluded_target_by_dependency(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_executable(hello SOURCES "hello.c" LINK_LIBRARIES PRIVATE Host::world)
    add_host_library(world STATIC SOURCES "world.c" EXCLUDE_FROM_ALL)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("hello.c", "int main() { return 0; }")
    testing.write("world.c", "int world() { return 0; }")
    testing.configure_internal().check_returncode()
    assert 'Linking HOSTC static library libworld.a' in testing.cmake("host-targets", verbose=True).stdout
