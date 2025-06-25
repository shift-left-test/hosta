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
    add_host_library(hello STATIC SOURCES hello.c)
    add_host_library(hello STATIC SOURCES hello.c)
    '''
    testing.write("hello.c", "void hello() {}")
    testing.write("CMakeLists.txt", content)
    assert 'add_custom_target cannot create target "HOST-hello"' in testing.configure_internal().stderr

def test_host_namespace_target(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(Host::hello STATIC SOURCES hello.c)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert 'Linking HOSTC static library libhello.a' in testing.cmake("host-targets", verbose=True).stdout

def test_unknown_type(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello unknown SOURCES hello.c)
    '''
    testing.write("hello.c", "void hello() {}")
    testing.write("CMakeLists.txt", content)
    assert 'Unsupported library type: unknown' in testing.configure_internal().stderr

def test_static_no_source(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC)
    '''
    testing.write("CMakeLists.txt", content)
    assert 'No SOURCES given to target: hello' in testing.configure_internal().stderr

def test_static_unknown_source(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES unknown.c)
    '''
    testing.write("CMakeLists.txt", content)
    assert 'Cannot find source file:\n\n    unknown.c' in testing.configure_internal().stderr

def test_static_sources(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main STATIC SOURCES hello.c world.c)
    '''
    testing.write("hello.c", "void hello() { }")
    testing.write("world.c", "void world() { }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()

def test_static_include_directories(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c INCLUDE_DIRECTORIES PUBLIC first second)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert f'-I{testing.workspace}/first -I{testing.workspace}/second' in testing.cmake("host-targets", verbose=True).stdout

def test_static_compile_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c COMPILE_OPTIONS PUBLIC -DHELLO)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert '-DHELLO' in testing.cmake("host-targets", verbose=True).stdout

def test_static_link_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c LINK_OPTIONS PUBLIC -fprofile-arcs -lm)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    testing.cmake("host-targets").check_returncode()

def test_static_link_static_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main STATIC SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello Host::world)
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
    assert f'-fprofile-arcs {testing.build}/libhello.a -lm' not in stdout  # No link options

def test_static_link_interface_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main STATIC SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello Host::world)
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
    assert '-fprofile-arcs -lm' not in stdout  # No link options

def test_static_link_libraries_with_private_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main STATIC SOURCES main.c LINK_LIBRARIES PRIVATE Host::hello)
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

def test_static_rebuild(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert 'Linking HOSTC static library' in testing.cmake("host-targets").stdout
    assert not 'Linking HOSTC static library' in testing.cmake("host-targets").stdout

def test_interface_sources(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE SOURCES hello.c)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    assert 'add_host_library INTERFACE requires no source arguments.' in testing.configure_internal().stderr

def test_interface_include_directories(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(CMakePrintHelpers)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE INCLUDE_DIRECTORIES PRIVATE a PUBLIC b)
    get_host_target_properties(Host::hello
      INCLUDE_DIRECTOIRES A
      INTERFACE_INCLUDE_DIRECTORIES B
    )
    cmake_print_variables(A B)
    '''
    testing.write("CMakeLists.txt", content)
    assert f'A="" ; B="{testing.workspace}/b"' in testing.configure_internal().stdout

def test_interface_compile_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(CMakePrintHelpers)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE COMPILE_OPTIONS PRIVATE a PUBLIC b)
    get_host_target_properties(Host::hello
      COMPILE_OPTIONS A
      INTERFACE_COMPILE_OPTIONS B
    )
    cmake_print_variables(A B)
    '''
    testing.write("CMakeLists.txt", content)
    assert f'A="" ; B="b"' in testing.configure_internal().stdout

def test_interface_link_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(CMakePrintHelpers)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE LINK_OPTIONS PRIVATE a PUBLIC b)
    get_host_target_properties(Host::hello
      LINK_OPTIONS A
      INTERFACE_LINK_OPTIONS B
    )
    cmake_print_variables(A B)
    '''
    testing.write("CMakeLists.txt", content)
    assert f'A="" ; B="b"' in testing.configure_internal().stdout

def test_interface_link_static_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main INTERFACE LINK_LIBRARIES PRIVATE Host::hello Host::world)
    add_host_library(hello STATIC SOURCES hello/hello.c INCLUDE_DIRECTORIES PUBLIC hello COMPILE_OPTIONS PUBLIC -DHELLO LINK_OPTIONS PUBLIC -fprofile-arcs)
    add_host_library(world STATIC SOURCES world/world.c INCLUDE_DIRECTORIES PUBLIC world COMPILE_OPTIONS PUBLIC -DWORLD LINK_OPTIONS PUBLIC -lm)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("hello/hello.h", "void hello();")
    testing.write("hello/hello.c", "void hello() { }")
    testing.write("world/world.h", "void world();")
    testing.write("world/world.c", "void world() { }")

    testing.configure_internal().check_returncode()
    process = testing.cmake("host-targets", verbose=True)
    process.check_returncode()
    stdout = process.stdout
    assert f'-I{testing.workspace}/hello -I{testing.workspace}/world' not in stdout  # No include directories
    assert '-DHELLO -DWORLD' not in stdout  # No compile options
    assert f'-fprofile-arcs {testing.build}/libhello.a -lm' not in stdout  # No link options

def test_interface_link_interface_libraries(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main INTERFACE LINK_LIBRARIES PRIVATE Host::hello Host::world)
    add_host_library(hello INTERFACE INCLUDE_DIRECTORIES PUBLIC hello COMPILE_OPTIONS PUBLIC -DHELLO LINK_OPTIONS PUBLIC -fprofile-arcs)
    add_host_library(world INTERFACE INCLUDE_DIRECTORIES PUBLIC world COMPILE_OPTIONS PUBLIC -DWORLD LINK_OPTIONS PUBLIC -lm)
    '''
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    process = testing.cmake("host-targets", verbose=True)
    process.check_returncode()
    stdout = process.stdout
    assert f'-I{testing.workspace}/hello -I{testing.workspace}/world' not in stdout  # No include directories
    assert '-DHELLO -DWORLD' not in stdout  # No compile options
    assert '-fprofile-arcs -lm' not in stdout  # No link options

def test_interface_link_libraries_with_private_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main INTERFACE LINK_LIBRARIES PRIVATE Host::hello)
    add_host_library(hello INTERFACE INCLUDE_DIRECTORIES PRIVATE aaa COMPILE_OPTIONS PRIVATE bbb LINK_OPTIONS PRIVATE ccc)
    '''
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    process = testing.cmake("host-targets", verbose=True)
    process.check_returncode()
    stdout = process.stdout
    assert '-I' not in stdout
    assert 'aaa' not in stdout
    assert 'bbb' not in stdout
    assert 'ccc' not in stdout

def test_interface_rebuild(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE)
    '''
    testing.write("CMakeLists.txt", content)
    testing.configure_internal().check_returncode()
    assert 'Scanning dependencies of target HOST-hello' in testing.cmake("host-targets").stdout
    assert not 'Scanning dependencies of target HOST-hello' in testing.cmake("host-targets").stdout

def test_cmake_host_flags(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)

    set(CMAKE_HOSTC_FLAGS "-DHOSTC_FLAGS_1;-DHOSTC_FLAGS_2")
    set(CMAKE_HOSTCXX_FLAGS "-DHOSTCXX_FLAGS_1;-DHOSTCXX_FLAGS_2")

    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES "{c_file}" "{cxx_file}")
    '''
    testing.write("CMakeLists.txt", content.format(c_file="c.c", cxx_file="cxx.cc"))
    testing.write("c.c", "int c() { return 0; }")
    testing.write("cxx.cc", "int cxx() { return 0; }")
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("host-targets", verbose=True).stdout
    assert '-DHOSTC_FLAGS_1 -DHOSTC_FLAGS_2' in stdout
    assert '-DHOSTCXX_FLAGS_1 -DHOSTCXX_FLAGS_2' in stdout

def test_cmake_host_static_linker_flags(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)

    set(CMAKE_HOST_STATIC_LINKER_FLAGS "-fno-common -fno-builtin")

    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES "{c_file}" "{cxx_file}")
    '''
    testing.write("CMakeLists.txt", content.format(c_file="c.c", cxx_file="cxx.cc"))
    testing.write("c.c", "int c() { return 0; }")
    testing.write("cxx.cc", "int cxx() { return 0; }")
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("host-targets", verbose=True).stdout
    assert not '-fno-common -fno-builtin' in stdout  # static linker (ar) does not use the flags

def test_cmake_host_include_path(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)

    set(CMAKE_HOST_INCLUDE_PATH "/include/first;/include/second")

    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES "{c_file}" "{cxx_file}")
    '''
    testing.write("CMakeLists.txt", content.format(c_file="c.c", cxx_file="cxx.cc"))
    testing.write("c.c", "int c() { return 0; }")
    testing.write("cxx.cc", "int cxx() { return 0; }")
    testing.configure_internal().check_returncode()
    stdout = testing.cmake("host-targets", verbose=True).stdout
    assert '-I/include/first -I/include/second' in stdout

def test_execlude_from_all_target(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES "hello.c" EXCLUDE_FROM_ALL)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("hello.c", "int hello() { return 0; }")
    testing.configure_internal().check_returncode()
    assert 'Nothing to be done' in testing.cmake("host-targets", verbose=True).stdout

def test_build_excluded_target_by_dependency(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES "hello.c" LINK_LIBRARIES PRIVATE Host::world)
    add_host_library(world STATIC SOURCES "world.c" EXCLUDE_FROM_ALL)
    '''
    testing.write("CMakeLists.txt", content)
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("world.c", "int world() { return 0; }")
    testing.configure_internal().check_returncode()
    assert 'Linking HOSTC static library libworld.a' in testing.cmake("host-targets", verbose=True).stdout
