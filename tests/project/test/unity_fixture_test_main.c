#include "unity_fixture.h"
#include "calc.h"

// Dummy functions to test regex matcher
// These functions should not be added to CTest
void asdfTEST(int a) {
  TEST_ASSERT_EQUAL_DOUBLE(0.5, divide(1, 2));
}

void asdf_TEST(int a) {
  TEST_ASSERT_EQUAL_DOUBLE(0.5, divide(1, 2));
}

// First group test suite
TEST_GROUP(FirstGroup);

TEST_SETUP(FirstGroup) {
}

TEST_TEAR_DOWN(FirstGroup) {
}

TEST
(FirstGroup, test_plus) {
  TEST_ASSERT_EQUAL(3, plus(1, 2));
}

IGNORE_TEST(FirstGroup, test_minus) {
  TEST_ASSERT_EQUAL(-1, minus(1, 2));
}

TEST_GROUP_RUNNER(FirstGroup) {
  RUN_TEST_CASE(FirstGroup, test_plus);
  RUN_TEST_CASE(FirstGroup, test_minus);
}

// Second group test suite
TEST_GROUP(SecondGroup);

TEST_SETUP(SecondGroup) {
}

TEST_TEAR_DOWN(SecondGroup) {
}

TEST(SecondGroup, test_multiply) {
  TEST_ASSERT_EQUAL(2, multiply(1, 2));
}

TEST(SecondGroup, test_divide) {
  TEST_ASSERT_EQUAL_DOUBLE(0.5, divide(1, 2));
}

TEST_GROUP_RUNNER(SecondGroup) {
  RUN_TEST_CASE(SecondGroup, test_multiply);
  // RUN_TEST_CASE(SecondGroup, test_divide);  // This line is intentionally removed for testing
  #if 0
  RUN_TEST_CASE(SecondGroup, test_divide);  // This line is intentionally added for testing
  #endif
}

static void runAllTests(void) {
  RUN_TEST_GROUP(FirstGroup);
  RUN_TEST_GROUP(SecondGroup);
}

int main(int argc, const char* argv[]) {
  return UnityMain(argc, argv, runAllTests);
}
