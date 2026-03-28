# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hosta** (v1.4.0) is a CMake framework for building and running C/C++ unit tests on the host platform, even within cross-compilation environments. The core product is a set of CMake scripts (in `cmake/`) that provide `add_host_executable()`, `add_host_library()`, and test integration functions for Unity and Google Test frameworks.

## Commands

### Run all tests
```bash
pytest -n auto
```

### Run a single test file
```bash
pytest tests/add_host_executable_test.py -xvv
```

### Run a specific test
```bash
pytest tests/add_host_executable_test.py::test_name -xvv
```

### Docker development environment
```bash
docker build -t host-test-dev .
docker run --rm -it -v `pwd`:/test host-test-dev
```

## Architecture

### Core CMake Framework (`cmake/`)

The framework is a pipeline: compiler detection -> compilation -> linking -> test registration.

- **HostBuild.cmake** — Main entry point. Provides `add_host_executable()` and `add_host_library()`. Handles object compilation, linking, dependency resolution, and custom target properties (`HOST_TYPE`, `HOST_NAME`, `HOST_SOURCES`, etc.). Uses `Host::` namespace prefix for targets, `HOST-` prefix internally.
- **HostTest.cmake** — Test integration layer. Provides `add_host_test()`, `unity_fixture_add_host_tests()`, `unity_fixture_discover_host_tests()`, `gtest_add_host_tests()`, `gtest_discover_host_tests()`. Registers tests with CTest.
- **HostCompilerUtilities.cmake** — Shared utilities: logging, compiler detection helpers, ABI compatibility, file dependency resolution, include flag generation.
- **DetermineHOSTCCompiler.cmake / DetermineHOSTCXXCompiler.cmake** — Auto-detect host C/C++ compilers independent of the cross-compilation toolchain.
- **UnityFixtureAddTests.cmake** — Runtime test discovery script for Unity fixture tests (invoked by CTest).

### Test Suite (`tests/`)

Tests are Python (pytest) and exercise the CMake framework by configuring, building, and running CMake projects in temporary directories. The `conftest.py` provides a `CMakeFixture` class (via `testing` fixture) that:
- Copies `tests/project/` template into a tmpdir workspace
- Runs `cmake -S ... -B ...` configuration
- Builds targets via `cmake --build`
- Runs tests via `ctest`
- Generates coverage via `gcovr`

Test files follow the pattern `*_test.py`. The test project template in `tests/project/` contains a calculator app with both C and C++ implementations, Unity tests, and Google Test tests.

### Sample Project (`sample/`)

A reference implementation showing how to use hosta in a real project with Unity, Google Test, and fff (Fake Function Framework).
