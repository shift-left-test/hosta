# Expression Calculator — hosta Sample Project

This sample project demonstrates how to use the **hosta** CMake framework to build and test C/C++ code on the host platform within a cross-compilation environment.

The project implements an expression calculator that evaluates mathematical expressions like `1 + 2 * (3 - 4)` from a string input.

## What This Demonstrates

| hosta Feature | Where |
|---------------|-------|
| `add_host_library(INTERFACE)` | `error` — shared error types (header-only) |
| `add_host_library(STATIC)` | `tokenizer`, `parser` — static archives |
| `add_host_library(SHARED)` + VERSION/SOVERSION | `eval` — shared library with versioning |
| `add_host_executable` | `calc` — CLI executable, test executables |
| `Host::` dependencies | All targets link via `Host::` namespace |
| `add_host_test` | Unity tokenizer test |
| `unity_fixture_add_host_tests` | Unity Fixture parser tests |
| `gtest_add_host_tests` | Google Test evaluator + integration tests |
| INTERFACE coverage library | Code coverage via compile/link options |
| Automatic RPATH | `calc` executable finds `libeval.so` at runtime |

## Architecture

```
Input: "1 + 2 * (3 - 4)"
         │
         ▼
   ┌───────────┐
   │ Tokenizer  │  STATIC library (libtokenizer.a)
   │            │  String → Token list
   └─────┬─────┘
         │
         ▼
   ┌───────────┐
   │  Parser    │  STATIC library (libparser.a)
   │            │  Token list → AST
   └─────┬─────┘
         │
         ▼
   ┌───────────┐
   │ Evaluator  │  SHARED library (libeval.so.1.0.0)
   │            │  AST → double result
   └─────┬─────┘
         │
         ▼
   Result: -1
```

## Supported Expressions

- Arithmetic: `+`, `-`, `*`, `/`
- Parentheses: `(`, `)`
- Decimal numbers: `3.14`, `.5`, `2.`
- Unary minus: `-3`, `-(2 + 1)`
- Operator precedence: `*` and `/` bind tighter than `+` and `-`

## Error Handling

| Error | Example |
|-------|---------|
| Invalid character | `1 + @` |
| Unexpected token | `1 + + 2` |
| Missing parenthesis | `(1 + 2` |
| Empty expression | `` |
| Division by zero | `1 / 0` |

## Building

```bash
cd sample
cmake -S . -B build
cmake --build build --target host-targets
```

## Running Tests

```bash
cd sample/build
ctest --output-on-failure
```

## Running the Calculator

```bash
cd sample/build
./calc
> 1 + 2 * (3 - 4)
= -1
> 3.14 * (2 + 1)
= 9.42
> q
```

## Project Structure

```
sample/
├── CMakeLists.txt              # Root: cross-compiler setup + hosta includes
├── error/
│   └── error.h                 # Error codes and result type
├── tokenizer/
│   ├── tokenizer.h             # Tokenizer API
│   └── tokenizer.c             # String → tokens
├── parser/
│   ├── parser.h                # Parser API and AST types
│   └── parser.c                # Recursive descent parser
├── evaluator/
│   ├── evaluator.h             # Evaluator API
│   └── evaluator.c             # AST tree-walk evaluator
├── calculator/
│   └── main.c                  # Interactive CLI
├── test/
│   ├── unity_test_main.c       # Tokenizer tests (Unity)
│   ├── unity_fixture_test_main.c # Parser tests (Unity Fixture)
│   └── googletest_main.cpp     # Evaluator + integration (Google Test)
└── external/
    ├── unity/                  # Unity test framework
    ├── fff/                    # Fake Function Framework
    └── gtest/                  # Google Test framework
```
