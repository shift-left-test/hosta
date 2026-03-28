#include <gtest/gtest.h>

extern "C" {
#include "evaluator.h"
#include "parser.h"
}

class EvaluatorTest : public ::testing::Test {
 protected:
  TokenList tl;
  ParseResult pr;
};

TEST_F(EvaluatorTest, evaluate_number) {
  tl = tokenize("42");
  pr = parse(&tl);
  ExprResult r = evaluate(pr.root);
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(42.0, r.value);
}

TEST_F(EvaluatorTest, evaluate_addition) {
  tl = tokenize("1 + 2");
  pr = parse(&tl);
  ExprResult r = evaluate(pr.root);
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(3.0, r.value);
}

TEST_F(EvaluatorTest, evaluate_division_by_zero) {
  tl = tokenize("1 / 0");
  pr = parse(&tl);
  ExprResult r = evaluate(pr.root);
  EXPECT_EQ(EXPR_ERROR_DIVISION_BY_ZERO, r.error);
}

TEST_F(EvaluatorTest, evaluate_unary_minus) {
  tl = tokenize("-5");
  pr = parse(&tl);
  ExprResult r = evaluate(pr.root);
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(-5.0, r.value);
}

TEST_F(EvaluatorTest, evaluate_null_node) {
  ExprResult r = evaluate(NULL);
  EXPECT_EQ(EXPR_ERROR_EMPTY_EXPRESSION, r.error);
}

class IntegrationTest : public ::testing::Test {};

TEST_F(IntegrationTest, simple_addition) {
  ExprResult r = evaluate_expression("1 + 2");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(3.0, r.value);
}

TEST_F(IntegrationTest, operator_precedence) {
  ExprResult r = evaluate_expression("1 + 2 * 3");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(7.0, r.value);
}

TEST_F(IntegrationTest, parentheses) {
  ExprResult r = evaluate_expression("(1 + 2) * 3");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(9.0, r.value);
}

TEST_F(IntegrationTest, complex_expression) {
  ExprResult r = evaluate_expression("1 + 2 * (3 - 4)");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(-1.0, r.value);
}

TEST_F(IntegrationTest, decimal_numbers) {
  ExprResult r = evaluate_expression("3.14 * (2 + 1)");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_NEAR(9.42, r.value, 0.001);
}

TEST_F(IntegrationTest, nested_parentheses) {
  ExprResult r = evaluate_expression("((2 + 3) * (4 - 1))");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(15.0, r.value);
}

TEST_F(IntegrationTest, unary_minus_expression) {
  ExprResult r = evaluate_expression("-(1 + 2)");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(-3.0, r.value);
}

TEST_F(IntegrationTest, division_with_decimals) {
  ExprResult r = evaluate_expression("7 / 2");
  EXPECT_EQ(EXPR_OK, r.error);
  EXPECT_DOUBLE_EQ(3.5, r.value);
}

TEST_F(IntegrationTest, error_invalid_char) {
  ExprResult r = evaluate_expression("1 + @");
  EXPECT_EQ(EXPR_ERROR_INVALID_CHAR, r.error);
}

TEST_F(IntegrationTest, error_division_by_zero) {
  ExprResult r = evaluate_expression("1 / 0");
  EXPECT_EQ(EXPR_ERROR_DIVISION_BY_ZERO, r.error);
}

TEST_F(IntegrationTest, error_missing_paren) {
  ExprResult r = evaluate_expression("(1 + 2");
  EXPECT_EQ(EXPR_ERROR_MISSING_PAREN, r.error);
}

TEST_F(IntegrationTest, error_empty) {
  ExprResult r = evaluate_expression("");
  EXPECT_EQ(EXPR_ERROR_EMPTY_EXPRESSION, r.error);
}

int main(int argc, char *argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
