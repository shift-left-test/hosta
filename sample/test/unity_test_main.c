#include "unity.h"
#include "tokenizer.h"

void setUp(void) {
}

void tearDown(void) {
}

void test_tokenize_single_number(void) {
  TokenList tl = tokenize("42");
  TEST_ASSERT_EQUAL(EXPR_OK, tl.error);
  TEST_ASSERT_EQUAL(2, tl.count);
  TEST_ASSERT_EQUAL(TOKEN_NUMBER, tl.tokens[0].type);
  TEST_ASSERT_EQUAL_DOUBLE(42.0, tl.tokens[0].value);
  TEST_ASSERT_EQUAL(TOKEN_END, tl.tokens[1].type);
}

void test_tokenize_decimal_number(void) {
  TokenList tl = tokenize("3.14");
  TEST_ASSERT_EQUAL(EXPR_OK, tl.error);
  TEST_ASSERT_EQUAL(TOKEN_NUMBER, tl.tokens[0].type);
  TEST_ASSERT_EQUAL_DOUBLE(3.14, tl.tokens[0].value);
}

void test_tokenize_simple_expression(void) {
  TokenList tl = tokenize("1 + 2");
  TEST_ASSERT_EQUAL(EXPR_OK, tl.error);
  TEST_ASSERT_EQUAL(4, tl.count);
  TEST_ASSERT_EQUAL(TOKEN_NUMBER, tl.tokens[0].type);
  TEST_ASSERT_EQUAL(TOKEN_PLUS, tl.tokens[1].type);
  TEST_ASSERT_EQUAL(TOKEN_NUMBER, tl.tokens[2].type);
  TEST_ASSERT_EQUAL(TOKEN_END, tl.tokens[3].type);
}

void test_tokenize_all_operators(void) {
  TokenList tl = tokenize("1+2-3*4/5");
  TEST_ASSERT_EQUAL(EXPR_OK, tl.error);
  TEST_ASSERT_EQUAL(10, tl.count);
  TEST_ASSERT_EQUAL(TOKEN_PLUS, tl.tokens[1].type);
  TEST_ASSERT_EQUAL(TOKEN_MINUS, tl.tokens[3].type);
  TEST_ASSERT_EQUAL(TOKEN_STAR, tl.tokens[5].type);
  TEST_ASSERT_EQUAL(TOKEN_SLASH, tl.tokens[7].type);
}

void test_tokenize_parentheses(void) {
  TokenList tl = tokenize("(1 + 2)");
  TEST_ASSERT_EQUAL(EXPR_OK, tl.error);
  TEST_ASSERT_EQUAL(TOKEN_LPAREN, tl.tokens[0].type);
  TEST_ASSERT_EQUAL(TOKEN_RPAREN, tl.tokens[4].type);
}

void test_tokenize_whitespace_handling(void) {
  TokenList tl = tokenize("  1  +  2  ");
  TEST_ASSERT_EQUAL(EXPR_OK, tl.error);
  TEST_ASSERT_EQUAL(4, tl.count);
}

void test_tokenize_invalid_character(void) {
  TokenList tl = tokenize("1 + @");
  TEST_ASSERT_EQUAL(EXPR_ERROR_INVALID_CHAR, tl.error);
  TEST_ASSERT_EQUAL(4, tl.error_pos);
}

void test_tokenize_position_tracking(void) {
  TokenList tl = tokenize("12 + 34");
  TEST_ASSERT_EQUAL(0, tl.tokens[0].pos);
  TEST_ASSERT_EQUAL(3, tl.tokens[1].pos);
  TEST_ASSERT_EQUAL(5, tl.tokens[2].pos);
}

int main(void) {
  UNITY_BEGIN();
  RUN_TEST(test_tokenize_single_number);
  RUN_TEST(test_tokenize_decimal_number);
  RUN_TEST(test_tokenize_simple_expression);
  RUN_TEST(test_tokenize_all_operators);
  RUN_TEST(test_tokenize_parentheses);
  RUN_TEST(test_tokenize_whitespace_handling);
  RUN_TEST(test_tokenize_invalid_character);
  RUN_TEST(test_tokenize_position_tracking);
  return UNITY_END();
}
