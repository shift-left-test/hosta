#include "CppUTest/TestHarness.h"
#include "CppUTest/CommandLineTestRunner.h"
#include "calc.hpp"

static Calculator calculator;

TEST_GROUP(CppUTestCalc) { };

TEST(CppUTestCalc, test_plus) {
  LONGS_EQUAL(3, calculator.plus(1, 2));
}

IGNORE_TEST(CppUTestCalc, test_minus) {
  LONGS_EQUAL(-1, calculator.minus(1, 2));
}

TEST(CppUTestCalc, test_multiply) {
  LONGS_EQUAL(2, calculator.multiply(1, 2));
}

TEST(CppUTestCalc, test_divide) {
  DOUBLES_EQUAL(0.5, calculator.divide(1, 2), 0.001);
}

int main(int ac, char** av) {
  return CommandLineTestRunner::RunAllTests(ac, av);
}
