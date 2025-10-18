# hosta

> Host based test automation for C/C++

## About

`hosta` is a comprehensive solution for building and executing unit tests for C/C++ programs using the host build toolchain. It leverages CMake scripts to facilitate the creation of test programs and their execution on the host platform via CTest, even within a cross-build toolchain environment.

## Features

- Comprehensive solution for building and running unit tests for C/C++ projects
- Uses CMake scripts for test execution on the host platform via CTest
- Supports dual-targeting in cross-build toolchain environments
- Provides functions to define host executables and libraries with ease
- Integrates with popular testing frameworks such as Unity and Google Test

## Prerequisites

Ensure the following software packages are installed on your host environment:

- CMake (3.16 or higher)
- C Compiler Toolchain (e.g. GCC, clang)
- C++ Compiler Toolchain (e.g. G++, clang++)

The following additional packages are required for testing this project:

- build-essential
- clang
- docker
- g++
- g++-mingw-w64
- gcc
- gcc-mingw-w64
- gcovr
- ninja-build
- pytest3
- pytest3-xdist
- python3

### Docker Setup

To streamline the setup process, you can build a Docker image with the necessary packages using the following commands:

```bash
$ docker build -t host-test-dev .
$ docker run --rm -it -v `pwd`:/test host-test-dev
$ cd /test
```

## Setup Instructions

To integrate `hosta` into your project, follow these steps:

Copy the files from the cmake directory to your project's CMake script directory.
Add the following line to your top-level CMakeLists.txt file:

```cmake
include(cmake/HostTest.cmake)
```

## Usage

### Creating an Executable for the Host Platform

To define an executable target for the host platform, use the `add_host_executbale` function:

```cmake
add_host_executable(<target>
  [SOURCES <source>...]
  [INCLUDE_DIRECTORIES <PRIVATE|PUBLIC> <include_directory>...]
  [COMPILE_OPTIONS <PRIVATE|PUBLIC> <compile_option>...]
  [LINK_OPTIONS <PRIVATE|PUBLIC> <link_option>...]
  [LINK_LIBRARIES <PRIVATE|PUBLIC> <library>...]
  [DEPENDS <depend>...]
  [EXCLUDE_FROM_ALL]
)

# Parameters:
# - target: Specifies the name of the executable target
# - sources: List of source files
# - include_directories: List of include directories
# - compile_options: List of compile options
# - link_options: List of link options
# - libraries: List of host libraries
# - depends: List of dependencies
# - EXCLUDE_FROM_ALL: Do not include the binary in the default build target

# Scope:
# - Arguments following both PRIVATE and PUBLIC are used to build the current target.
```

### Creating a Library for the Host Platform

To define a library target for the host platform, use the `add_host_library` function:

```cmake
add_host_library(<target> <type>
  [SOURCES <source>...]
  [INCLUDE_DIRECTORIES <PRIVATE|PUBLIC> <include_directory>...]
  [COMPILE_OPTIONS <PRIVATE|PUBLIC> <compile_option>...]
  [LINK_OPTIONS <PRIVATE|PUBLIC> <link_option>...]
  [LINK_LIBRARIES <PRIVATE|PUBLIC> <library>...]
  [DEPENDS <depend>...]
  [EXCLUDE_FROM_ALL]
)

# Parameters:
# - target: Specifies the name of the library target
# - type: Type of the library (e.g. STATIC, INTERFACE)
# - sources: List of source files (Note: INTERFACE library requires no source files)
# - include_directories: List of include directories
# - compile_options: List of compile options
# - link_options: List of link options
# - libraries: List of host libraries
# - depends: List of dependencies
# - EXCLUDE_FROM_ALL: Do not include the binary in the default build target

# Scope:
# - Arguments following both PRIVATE and PUBLIC are used to build the current target.
# - Arguments following PUBLIC are also used to build another target that links to the current target.
```

### Host Target Dependencies

The host functions, such as `add_host_library` and `add_host_executable`, create target names with the virtual namespace prefix `Host::` to distinguish them from ordinary target names. The host target names are used to define dependencies between host targets. For instance, the following code demonstrates how to create a host executable named `hello` that depends on a host library named `world`.

```cmake
add_host_executable(hello
  SOURCES hello.c
  LINK_LIBRARIES Host::world
)

add_host_library(world STATIC
  SOURCES world.c
)
```

#### Limitations

- Only direct dependencies between host targets are allowed. Indirect dependencies are not properly reflected.
- Only host libraries are allowed for LINK_LIBRARIES. Non-host libraries are not permitted even if they are host-compatible. Non-existing host libraries cause build failures.

### Adding an Executable as a Test with CTest

To add an executable target as a test with CTest, use the `add_host_test` function:

```cmake
add_host_test(<target> [PREFIX <prefix>] [EXTRA_ARGS <extra_args>...])

# Parameters:
# - target: Specifies the name of the executable target created with `add_host_executable`
# - PREFIX: Specifies a prefix to be prepended to the test case name
# - EXTRA_ARGS: Any additional arguments to pass on the command line
```

### Adding an Executable as Tests for Unity Fixture Test Macros

To automatically add an executable target as tests with CTest by scanning the source code for Unity fixture test macros, use the `unity_fixture_add_host_tests` function:

```cmake
unity_fixture_add_host_tests(<target> [PREFIX <prefix>] [EXTRA_ARGS <extra_args>...])

# Parameters:
# - target: Specifies the name of the executable target created with `add_host_executable`
# - PREFIX: Specifies a prefix to be prepended to the name of each test case
# - EXTRA_ARGS: Any additional arguments to pass on the command line
```

To dynamically discover tests that should be executed from an executable target, use the `unity_fixture_discover_host_tests` function:

```cmake
unity_fixture_discover_host_tests(<target> [PREFIX <prefix>] [WORKING_DIRECTORY <directory>] [TEST_LIST <name>] [DISCOVERY_TIMEOUT <second>] [EXTRA_ARGS <extra_args>...] [PROPERTIES <properties>...]

# Parameters:
# - target: Specifies the name of the executable target created with `add_host_executable`
# - PREFIX: Specifies a prefix to be prepended to the name of each test case
# - WORKING_DIRECTORY: Specifies the directory in which to run the discovered tests
# - TEST_LIST: Make the list of tests available in this variable, instead of the default `<target>_TESTS`
# - DISCOVERY_TIMEOUT: Specifies how long (in seconds) CMake will wait for the executable to enumerate available tests
# - EXTRA_ARGS: Any extra arguments to pass on the command line to each test case
# - PROPERTIES: Specifies additional properties to be set on all discovered tests
```

This feature requires -d (dry-run) option provided by Unity fixture. Make sure that Unity fixture version supports this option before using the feature.
You may refer to [this link](https://github.com/ThrowTheSwitch/Unity/tree/master/extras/fixture) for more information about the Unity fixture.

### Adding an Executable as Tests with CTest for Google Test Macros

To automatically add an executable target as tests with CTest by scanning the source code for Google test macros, use the `gtest_add_host_tests` function:

```cmake
gtest_add_host_tests(<target> [PREFIX <prefix>] [EXTRA_ARGS <extra_args>])

# Parameters:
# - target: Specifies the name of the executable target created with `add_host_executable`
# - prefix: Specifies a prefix to be prepended to the name of each test case
# - extra_args: Any additional arguments to pass on the command line
```

To dynamically discover tests that should be executed from an executable target, use the `gtest_discover_host_tests` function:

```cmake
gtest_discover_host_tests(<target> [PREFIX <prefix>] [NO_PRETTY_TYPES] [NO_PRETTY_VALUES] [WORKING_DIRECTORY <directory>] [TEST_LIST <name>] [DISCOVERY_TIMEOUT <second>] [EXTRA_ARGS <extra_args>...] [PROPERTIES <properties>...]

# Parameters:
# - target: Specifies the name of the executable target created with `add_host_executable`
# - PREFIX: Specifies a prefix to be prepended to the name of each test case
# - NO_PRETTY_TYPES: Uses the type index instead of the actual type name in type-parameterized test names
# - NO_PRETTY_VALUES: Use the value index instead of the actual value in value-parameterized test names
# - WORKING_DIRECTORY: Specifies the directory in which to run the discovered tests
# - TEST_LIST: Make the list of tests available in this variable, instead of the default `<target>_TESTS`
# - DISCOVERY_TIMEOUT: Specifies how long (in seconds) CMake will wait for the executable to enumerate available tests
# - EXTRA_ARGS: Any extra arguments to pass on the command line to each test case
# - PROPERTIES: Specifies additional properties to be set on all discovered tests
```

## CMake Variables

The following CMake variables can be used to configure internal behaviors:

- `CMAKE_HOST${lang}_COMPILER_LIST`: This variable is used to find the host compiler
- `CMAKE_HOST${lang}_EXTENSIONS`: Specifies whether compiler-specific extensions are required
- `CMAKE_HOST${lang}_FLAGS`: Specifies global compiler flags
- `CMAKE_HOST${lang}_OUTPUT_EXTENSION`: Defines the extension for object files
- `CMAKE_HOST${lang}_STANDARD`: Defines the language standard version
- `CMAKE_HOST_BUILD_TARGET`: Defines the target name to be used when building host targets (default: host-targets)
- `CMAKE_HOST_EXECUTABLE_SUFFIX`: Defines the extension for executable files
- `CMAKE_HOST_EXE_LINKER_FLAGS`: Defines global linker flags for executables
- `CMAKE_HOST_INCLUDE_PATH`: Specifies additional directories to search for header files for host targets
- `CMAKE_HOST_STATIC_LIBRARY_PREFIX`: Defines the prefix for static libraries
- `CMAKE_HOST_STATIC_LIBRARY_SUFFIX`: Defines the extension for static libraries
- `CMAKE_HOST_STATIC_LINKER_FLAGS`: Specifies global linker flags for static libraries
- `ENABLE_HOST_LANGUAGES`: Defines preferred host languages (default: C CXX)
- `ENABLE_HOST_UNITY_FIXTURE_EXACT_MATCH`: Only runs tests whose group and name exactly match the specified value (Note: This feature requires -G and -N options provided by Unity fixture. This is disabled by default for backward compatibility.)

## Building the Project

To build and execute sample tests, use the following commands:

```bash
$ cd sample
$ cmake .
$ make host-targets
$ ctest
```

## Testing the CMake Scripts

To test the CMake scripts, use the following command:

```bash
$ pytest -n auto
```

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.
