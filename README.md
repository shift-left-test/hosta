# hosta

> Host based test automation for C/C++

## Table of Contents

- [About](#about)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
  - [Creating an Executable](#creating-an-executable-for-the-host-platform)
  - [Creating a Library](#creating-a-library-for-the-host-platform)
    - [Library Types](#library-types)
    - [Shared Library Example](#shared-library-example)
  - [Host Target Dependencies](#host-target-dependencies)
  - [Adding Tests with CTest](#adding-an-executable-as-a-test-with-ctest)
  - [Unity Fixture Tests](#adding-an-executable-as-tests-for-unity-fixture-test-macros)
  - [Google Test](#adding-an-executable-as-tests-with-ctest-for-google-test-macros)
- [CMake Variables](#cmake-variables)
- [Building the Sample Project](#building-the-sample-project)
- [Testing the CMake Scripts](#testing-the-cmake-scripts)
- [License](#license)

## About

`hosta` is a CMake framework for building and running C/C++ unit tests on the **host platform**, even when your project uses a **cross-compilation toolchain**.

In cross-compilation environments (e.g., building for ARM with `arm-none-eabi-gcc`), unit tests cannot run on the developer's machine because the binaries are built for a different target. `hosta` solves this by automatically detecting and using the host compiler alongside the cross-compiler within the same CMake build, enabling you to compile and execute tests locally.

### Features

- Automatic host compiler detection independent of the cross-compilation toolchain
- Dual-targeting: cross-compile for the target platform and build tests for the host in one build
- Static, shared, and interface host libraries with full dependency management
- Shared library versioning (VERSION/SOVERSION), soname, and automatic RPATH handling
- Integration with [Unity](https://github.com/ThrowTheSwitch/Unity) and [Google Test](https://github.com/google/googletest) frameworks
- Test registration and execution through CTest

## Quick Start

Below is a minimal example showing how `hosta` enables host-based testing in a cross-compilation project:

```cmake
cmake_minimum_required(VERSION 3.17)

# Cross-compiler toolchain configuration
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_C_COMPILER i686-w64-mingw32-gcc)

project(my_project LANGUAGES C)

include(cmake/HostTest.cmake)
enable_testing()

# Build a host library for testing
add_host_library(mylib STATIC
  SOURCES src/mylib.c
  INCLUDE_DIRECTORIES PUBLIC src
)

# Build and register a test executable for the host
add_host_executable(mylib_test
  SOURCES test/mylib_test.c
  LINK_LIBRARIES PRIVATE Host::mylib Host::unity
)

add_host_test(Host::mylib_test)
```

```bash
cmake -S . -B build
cmake --build build --target host-targets
cd build && ctest
```

## Prerequisites

### For using hosta

- CMake (3.17 or higher)
- C/C++ host compiler toolchain (e.g., GCC, Clang)

### For developing hosta

The following additional packages are required for running the test suite:

- build-essential, gcc, g++, clang
- gcc-mingw-w64, g++-mingw-w64 (cross-compilation tests)
- ninja-build
- gcovr (coverage reports)
- python3, python3-pytest, python3-pytest-xdist

#### Docker Setup

To streamline the setup process, you can build a Docker image with all the necessary packages:

```bash
docker build -t host-test-dev .
docker run --rm -it -v `pwd`:/test host-test-dev
cd /test
```

## Setup Instructions

To integrate `hosta` into your project, follow these steps:

1. Copy the files from the `cmake/` directory to your project's CMake script directory.
2. Add the following line to your top-level `CMakeLists.txt` file:

```cmake
include(cmake/HostTest.cmake)
```

## Usage

### Creating an Executable for the Host Platform

To define an executable target for the host platform, use the `add_host_executable` function:

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
```

| Parameter | Description |
|-----------|-------------|
| `target` | Name of the executable target |
| `SOURCES` | List of source files |
| `INCLUDE_DIRECTORIES` | List of include directories |
| `COMPILE_OPTIONS` | List of compile options |
| `LINK_OPTIONS` | List of link options |
| `LINK_LIBRARIES` | List of host libraries |
| `DEPENDS` | List of dependencies |
| `EXCLUDE_FROM_ALL` | Do not include the binary in the default build target |

> **Scope:** Arguments following both `PRIVATE` and `PUBLIC` are used to build the current target.

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
  [VERSION <version>]
  [SOVERSION <soversion>]
  [EXCLUDE_FROM_ALL]
)
```

| Parameter | Description |
|-----------|-------------|
| `target` | Name of the library target |
| `type` | Type of the library (`STATIC`, `SHARED`, or `INTERFACE`) |
| `SOURCES` | List of source files (`INTERFACE` library requires no source files) |
| `INCLUDE_DIRECTORIES` | List of include directories |
| `COMPILE_OPTIONS` | List of compile options |
| `LINK_OPTIONS` | List of link options |
| `LINK_LIBRARIES` | List of host libraries |
| `DEPENDS` | List of dependencies |
| `VERSION` | Library version for `SHARED` libraries (e.g., `1.2.3`) |
| `SOVERSION` | SO version for `SHARED` libraries (e.g., `1`) |
| `EXCLUDE_FROM_ALL` | Do not include the binary in the default build target |

> **Scope:** Arguments following both `PRIVATE` and `PUBLIC` are used to build the current target. Arguments following `PUBLIC` are also used to build another target that links to the current target.

#### Library Types

| Type | Description |
|------|-------------|
| `STATIC` | A static archive (`.a`). Requires `SOURCES`. |
| `SHARED` | A shared library (`.so`/`.dylib`/`.dll`). Requires `SOURCES`. Automatically compiles with position-independent code (`-fPIC`). Supports `VERSION` and `SOVERSION` for soname and symlink management. |
| `INTERFACE` | A header-only library. Does not require `SOURCES`. Only `PUBLIC` properties are used. |

#### Shared Library Example

```cmake
add_host_library(mylib SHARED
  SOURCES src/mylib.c
  INCLUDE_DIRECTORIES PUBLIC src
  VERSION 1.2.3
  SOVERSION 1
)

add_host_executable(mylib_test
  SOURCES test/mylib_test.c
  LINK_LIBRARIES PRIVATE Host::mylib
)
```

When `VERSION` and `SOVERSION` are specified, the build produces:
- `libmylib.so.1.2.3` — the actual shared library
- `libmylib.so.1` — soname symlink
- `libmylib.so` — development symlink

RPATH is automatically set so that executables linked against host shared libraries can find them at runtime.

### Host Target Dependencies

The host functions create target names with the virtual namespace prefix `Host::` to distinguish them from ordinary target names. Use the `Host::` prefix when defining dependencies between host targets:

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

- Only **direct** dependencies between host targets are allowed. Indirect dependencies are not properly reflected.
- Only **host libraries** are allowed for `LINK_LIBRARIES`. Non-host libraries are not permitted even if they are host-compatible. Non-existing host libraries cause build failures.

### Adding an Executable as a Test with CTest

To add an executable target as a test with CTest, use the `add_host_test` function:

```cmake
add_host_test(<target> [PREFIX <prefix>] [EXTRA_ARGS <extra_args>...])
```

| Parameter | Description |
|-----------|-------------|
| `target` | Name of the executable target created with `add_host_executable` |
| `PREFIX` | Prefix to be prepended to the test case name |
| `EXTRA_ARGS` | Additional arguments to pass on the command line |

### Adding an Executable as Tests for Unity Fixture Test Macros

To automatically add an executable target as tests with CTest by scanning the source code for Unity fixture test macros, use the `unity_fixture_add_host_tests` function:

```cmake
unity_fixture_add_host_tests(<target> [PREFIX <prefix>] [EXTRA_ARGS <extra_args>...])
```

| Parameter | Description |
|-----------|-------------|
| `target` | Name of the executable target created with `add_host_executable` |
| `PREFIX` | Prefix to be prepended to the name of each test case |
| `EXTRA_ARGS` | Additional arguments to pass on the command line |

To dynamically discover tests at CTest runtime, use the `unity_fixture_discover_host_tests` function:

```cmake
unity_fixture_discover_host_tests(<target>
  [PREFIX <prefix>]
  [WORKING_DIRECTORY <directory>]
  [TEST_LIST <name>]
  [DISCOVERY_TIMEOUT <second>]
  [EXTRA_ARGS <extra_args>...]
  [PROPERTIES <properties>...]
)
```

| Parameter | Description |
|-----------|-------------|
| `target` | Name of the executable target created with `add_host_executable` |
| `PREFIX` | Prefix to be prepended to the name of each test case |
| `WORKING_DIRECTORY` | Directory in which to run the discovered tests |
| `TEST_LIST` | Variable name to store the list of tests (default: `<target>_TESTS`) |
| `DISCOVERY_TIMEOUT` | How long (in seconds) CMake will wait for the executable to enumerate available tests |
| `EXTRA_ARGS` | Extra arguments to pass on the command line to each test case |
| `PROPERTIES` | Additional properties to be set on all discovered tests |

> **Note:** This feature requires the `-d` (dry-run) option provided by Unity fixture. Make sure that your Unity fixture version supports this option before using the feature. See [Unity fixture](https://github.com/ThrowTheSwitch/Unity/tree/master/extras/fixture) for details.

### Adding an Executable as Tests with CTest for Google Test Macros

To automatically add an executable target as tests with CTest by scanning the source code for Google Test macros, use the `gtest_add_host_tests` function:

```cmake
gtest_add_host_tests(<target> [PREFIX <prefix>] [EXTRA_ARGS <extra_args>...])
```

| Parameter | Description |
|-----------|-------------|
| `target` | Name of the executable target created with `add_host_executable` |
| `PREFIX` | Prefix to be prepended to the name of each test case |
| `EXTRA_ARGS` | Additional arguments to pass on the command line |

To dynamically discover tests at CTest runtime, use the `gtest_discover_host_tests` function:

```cmake
gtest_discover_host_tests(<target>
  [PREFIX <prefix>]
  [NO_PRETTY_TYPES]
  [NO_PRETTY_VALUES]
  [WORKING_DIRECTORY <directory>]
  [TEST_LIST <name>]
  [DISCOVERY_TIMEOUT <second>]
  [EXTRA_ARGS <extra_args>...]
  [PROPERTIES <properties>...]
)
```

| Parameter | Description |
|-----------|-------------|
| `target` | Name of the executable target created with `add_host_executable` |
| `PREFIX` | Prefix to be prepended to the name of each test case |
| `NO_PRETTY_TYPES` | Use the type index instead of the actual type name in type-parameterized test names |
| `NO_PRETTY_VALUES` | Use the value index instead of the actual value in value-parameterized test names |
| `WORKING_DIRECTORY` | Directory in which to run the discovered tests |
| `TEST_LIST` | Variable name to store the list of tests (default: `<target>_TESTS`) |
| `DISCOVERY_TIMEOUT` | How long (in seconds) CMake will wait for the executable to enumerate available tests |
| `EXTRA_ARGS` | Extra arguments to pass on the command line to each test case |
| `PROPERTIES` | Additional properties to be set on all discovered tests |

## CMake Variables

The following CMake variables can be used to configure internal behaviors. `${lang}` refers to `C` or `CXX`.

### Compiler Configuration

| Variable | Description |
|----------|-------------|
| `CMAKE_HOST${lang}_COMPILER_LIST` | Compiler candidates for host compiler detection |
| `CMAKE_HOST${lang}_STANDARD` | Language standard version (e.g., `11`, `14`, `17`) |
| `CMAKE_HOST${lang}_EXTENSIONS` | Whether compiler-specific extensions are enabled |
| `CMAKE_HOST${lang}_FLAGS` | Global compiler flags |
| `CMAKE_HOST${lang}_OUTPUT_EXTENSION` | Extension for object files |
| `ENABLE_HOST_LANGUAGES` | Preferred host languages (default: `C CXX`) |

### Linker and Output Configuration

| Variable | Description |
|----------|-------------|
| `CMAKE_HOST_EXE_LINKER_FLAGS` | Global linker flags for executables |
| `CMAKE_HOST_STATIC_LINKER_FLAGS` | Global linker flags for static libraries |
| `CMAKE_HOST_SHARED_LINKER_FLAGS` | Global linker flags for shared libraries |
| `CMAKE_HOST_EXECUTABLE_SUFFIX` | Extension for executable files |
| `CMAKE_HOST_STATIC_LIBRARY_PREFIX` | Prefix for static libraries |
| `CMAKE_HOST_STATIC_LIBRARY_SUFFIX` | Extension for static libraries |
| `CMAKE_HOST_SHARED_LIBRARY_PREFIX` | Prefix for shared libraries |
| `CMAKE_HOST_SHARED_LIBRARY_SUFFIX` | Extension for shared libraries |
| `CMAKE_HOST_SKIP_BUILD_RPATH` | If set, do not add build directory RPATH for shared library dependencies |
| `CMAKE_HOST_BUILD_RPATH` | Custom RPATH to embed in host executables |

### Build Configuration

| Variable | Description |
|----------|-------------|
| `CMAKE_HOST_BUILD_TARGET` | Target name for building host targets (default: `host-targets`) |
| `CMAKE_HOST_INCLUDE_PATH` | Additional include directories for host targets |

### Test Configuration

| Variable | Description |
|----------|-------------|
| `ENABLE_HOST_UNITY_FIXTURE_EXACT_MATCH` | Only run tests whose group and name exactly match the specified value. Requires `-G` and `-N` options provided by Unity fixture. Disabled by default for backward compatibility. |

## Building the Sample Project

To build and execute sample tests, use the following commands:

```bash
cd sample
cmake .
make host-targets
ctest
```

## Testing the CMake Scripts

To run the full test suite:

```bash
pytest -n auto
```

To run a specific test file:

```bash
pytest tests/add_host_executable_test.py -xvv
```

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.
