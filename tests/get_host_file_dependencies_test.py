#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


content = '''
cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)
get_host_file_dependencies(C OUTPUT
  SOURCE {source}
  INCLUDE_DIRECTORIES {include_directories}
  COMPILE_OPTIONS {compile_options}
)

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_standalone_file(testing):
    testing.write("main.c", "int main() { return 0; }")
    testing.write("CMakeLists.txt", content.format(source="main.c", include_directories="", compile_options=""))
    assert f'OUTPUT="{testing.workspace}/main.c"' in testing.configure_internal().stdout

def test_dependency_in_same_directory(testing):
    testing.write("hello.h", "void hello() {}")
    testing.write("main.c", '#include "hello.h"\nint main() { hello(); return 0; }')
    testing.write("CMakeLists.txt", content.format(source="main.c", include_directories="", compile_options=""))
    assert f'OUTPUT="{testing.workspace}/main.c;{testing.workspace}/hello.h"' in testing.configure_internal().stdout

def test_include_dir_of_sub_directory(testing):
    testing.write("hello/hello.h", "void hello() {}")
    testing.write("main.c", '#include "hello/hello.h"\nint main() { hello(); return 0; }')
    testing.write("CMakeLists.txt", content.format(source="main.c", include_directories="", compile_options=""))
    assert f'OUTPUT="{testing.workspace}/main.c;{testing.workspace}/hello/hello.h"' in testing.configure_internal().stdout

def test_include_directories(testing):
    testing.write("hello/hello.h", "void hello() {}")
    testing.write("main.c", '#include "hello.h"\nint main() { hello(); return 0; }')
    testing.write("CMakeLists.txt", content.format(source="main.c", include_directories=f"-I{testing.workspace}/hello", compile_options=""))
    assert f'OUTPUT="{testing.workspace}/main.c;{testing.workspace}/hello/hello.h"' in testing.configure_internal().stdout

def test_compile_options_enabled(testing):
    testing.write("hello/hello.h", "void hello() {}")
    testing.write("main.c", '#ifdef HELLO\n #include "hello/hello.h"\n #endif\n int main() { hello(); return 0; }')
    testing.write("CMakeLists.txt", content.format(source="main.c", include_directories="", compile_options="-DHELLO"))
    assert f'OUTPUT="{testing.workspace}/main.c;{testing.workspace}/hello/hello.h"' in testing.configure_internal().stdout

def test_compile_options_disabled(testing):
    testing.write("hello/hello.h", "void hello() {}")
    testing.write("main.c", '#ifdef HELLO\n #include "hello/hello.h"\n #endif\n int main() { hello(); return 0; }')
    testing.write("CMakeLists.txt", content.format(source="main.c", include_directories="", compile_options=""))
    assert f'OUTPUT="{testing.workspace}/main.c"' in testing.configure_internal().stdout
