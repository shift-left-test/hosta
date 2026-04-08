# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

# Unity test: tokenizer
add_host_executable(unity_test
  SOURCES unity_test_main.c
  LINK_LIBRARIES PRIVATE Host::tokenizer Host::error Host::unity Host::coverage
)

add_host_test(Host::unity_test)

# Unity Fixture test: parser
add_host_executable(unity_fixture_test
  SOURCES unity_fixture_test_main.c
  LINK_LIBRARIES PRIVATE Host::parser Host::tokenizer Host::error Host::unity-fixture Host::unity Host::coverage
)

unity_fixture_add_host_tests(Host::unity_fixture_test)

# Google Test: evaluator + integration
add_host_executable(google_test
  SOURCES googletest_main.cpp
  LINK_LIBRARIES PRIVATE Host::eval Host::parser Host::tokenizer Host::error Host::gtest Host::coverage
)

gtest_add_host_tests(Host::google_test)
