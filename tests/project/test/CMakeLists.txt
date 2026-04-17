add_host_executable(no_unity_fixture_test
  SOURCES ../calculator/calc.c unity_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../calculator
  LINK_LIBRARIES PRIVATE Host::unity Host::coverage Host::hostc_options
)

unity_fixture_add_host_tests(no_unity_fixture_test)

add_host_executable(unity_fixture_test
  SOURCES ../calculator/calc.c unity_fixture_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../calculator
  LINK_LIBRARIES PRIVATE Host::unity-fixture Host::unity Host::coverage Host::hostc_options
)

unity_fixture_add_host_tests(unity_fixture_test PREFIX ${HOST_TEST_PREFIX})

add_host_executable(google_test
  SOURCES ../calculator/calc.cpp google_test_main.cpp
  INCLUDE_DIRECTORIES PRIVATE ../calculator
  LINK_LIBRARIES PRIVATE Host::gtest Host::coverage Host::hostcxx_options
  DEPENDS hello
)

gtest_add_host_tests(google_test PREFIX ${HOST_TEST_PREFIX})

add_host_executable(cpputest_test
  SOURCES ../calculator/calc.cpp cpputest_main.cpp
  INCLUDE_DIRECTORIES PRIVATE ../calculator
  LINK_LIBRARIES PRIVATE Host::cpputest Host::coverage Host::hostcxx_options
  DEPENDS hello
)

cpputest_add_host_tests(cpputest_test PREFIX ${HOST_TEST_PREFIX})
