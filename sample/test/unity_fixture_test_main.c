#include "unity_fixture.h"
#include "parser.h"

static TokenList tl;
static ParseResult pr;

TEST_GROUP(ParserBasic);

TEST_SETUP(ParserBasic) {
}

TEST_TEAR_DOWN(ParserBasic) {
}

TEST(ParserBasic, parse_single_number) {
  tl = tokenize("42");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_NOT_NULL(pr.root);
  TEST_ASSERT_EQUAL(NODE_NUMBER, pr.root->type);
  TEST_ASSERT_EQUAL_DOUBLE(42.0, pr.root->value);
}

TEST(ParserBasic, parse_decimal_number) {
  tl = tokenize("3.14");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_NUMBER, pr.root->type);
  TEST_ASSERT_EQUAL_DOUBLE(3.14, pr.root->value);
}

TEST(ParserBasic, parse_addition) {
  tl = tokenize("1 + 2");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_ADD, pr.root->type);
  TEST_ASSERT_EQUAL_DOUBLE(1.0, pr.root->left->value);
  TEST_ASSERT_EQUAL_DOUBLE(2.0, pr.root->right->value);
}

TEST(ParserBasic, parse_subtraction) {
  tl = tokenize("5 - 3");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_SUB, pr.root->type);
}

TEST(ParserBasic, parse_multiplication) {
  tl = tokenize("2 * 3");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_MUL, pr.root->type);
}

TEST(ParserBasic, parse_division) {
  tl = tokenize("6 / 2");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_DIV, pr.root->type);
}

TEST_GROUP_RUNNER(ParserBasic) {
  RUN_TEST_CASE(ParserBasic, parse_single_number);
  RUN_TEST_CASE(ParserBasic, parse_decimal_number);
  RUN_TEST_CASE(ParserBasic, parse_addition);
  RUN_TEST_CASE(ParserBasic, parse_subtraction);
  RUN_TEST_CASE(ParserBasic, parse_multiplication);
  RUN_TEST_CASE(ParserBasic, parse_division);
}

TEST_GROUP(ParserPrecedence);

TEST_SETUP(ParserPrecedence) {
}

TEST_TEAR_DOWN(ParserPrecedence) {
}

TEST(ParserPrecedence, mul_before_add) {
  tl = tokenize("1 + 2 * 3");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_ADD, pr.root->type);
  TEST_ASSERT_EQUAL(NODE_NUMBER, pr.root->left->type);
  TEST_ASSERT_EQUAL(NODE_MUL, pr.root->right->type);
}

TEST(ParserPrecedence, parentheses_override) {
  tl = tokenize("(1 + 2) * 3");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_MUL, pr.root->type);
  TEST_ASSERT_EQUAL(NODE_ADD, pr.root->left->type);
  TEST_ASSERT_EQUAL(NODE_NUMBER, pr.root->right->type);
}

TEST(ParserPrecedence, nested_parentheses) {
  tl = tokenize("((1 + 2))");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_ADD, pr.root->type);
}

TEST(ParserPrecedence, unary_minus) {
  tl = tokenize("-3");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_UNARY_MINUS, pr.root->type);
  TEST_ASSERT_EQUAL_DOUBLE(3.0, pr.root->left->value);
}

TEST(ParserPrecedence, unary_minus_in_expression) {
  tl = tokenize("-(1 + 2)");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_OK, pr.error);
  TEST_ASSERT_EQUAL(NODE_UNARY_MINUS, pr.root->type);
  TEST_ASSERT_EQUAL(NODE_ADD, pr.root->left->type);
}

TEST_GROUP_RUNNER(ParserPrecedence) {
  RUN_TEST_CASE(ParserPrecedence, mul_before_add);
  RUN_TEST_CASE(ParserPrecedence, parentheses_override);
  RUN_TEST_CASE(ParserPrecedence, nested_parentheses);
  RUN_TEST_CASE(ParserPrecedence, unary_minus);
  RUN_TEST_CASE(ParserPrecedence, unary_minus_in_expression);
}

TEST_GROUP(ParserErrors);

TEST_SETUP(ParserErrors) {
}

TEST_TEAR_DOWN(ParserErrors) {
}

TEST(ParserErrors, missing_closing_paren) {
  tl = tokenize("(1 + 2");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_ERROR_MISSING_PAREN, pr.error);
}

TEST(ParserErrors, empty_expression) {
  tl = tokenize("");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_ERROR_EMPTY_EXPRESSION, pr.error);
}

TEST(ParserErrors, unexpected_token) {
  tl = tokenize("1 + + 2");
  pr = parse(&tl);
  TEST_ASSERT_EQUAL(EXPR_ERROR_UNEXPECTED_TOKEN, pr.error);
}

TEST(ParserErrors, trailing_operator) {
  tl = tokenize("1 +");
  pr = parse(&tl);
  TEST_ASSERT_NOT_EQUAL(EXPR_OK, pr.error);
}

TEST_GROUP_RUNNER(ParserErrors) {
  RUN_TEST_CASE(ParserErrors, missing_closing_paren);
  RUN_TEST_CASE(ParserErrors, empty_expression);
  RUN_TEST_CASE(ParserErrors, unexpected_token);
  RUN_TEST_CASE(ParserErrors, trailing_operator);
}

static void runAllTests(void) {
  RUN_TEST_GROUP(ParserBasic);
  RUN_TEST_GROUP(ParserPrecedence);
  RUN_TEST_GROUP(ParserErrors);
}

int main(int argc, const char *argv[]) {
  return UnityMain(argc, argv, runAllTests);
}
