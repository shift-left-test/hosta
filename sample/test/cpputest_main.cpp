#include "CppUTest/TestHarness.h"
#include "CppUTest/CommandLineTestRunner.h"

extern "C" {
#include "tokenizer.h"
}

TEST_GROUP(TokenizerBasic) { };

TEST(TokenizerBasic, single_number) {
  TokenList tl = tokenize("42");
  LONGS_EQUAL(EXPR_OK, tl.error);
  LONGS_EQUAL(2, tl.count);
  LONGS_EQUAL(TOKEN_NUMBER, tl.tokens[0].type);
  DOUBLES_EQUAL(42.0, tl.tokens[0].value, 0.001);
  LONGS_EQUAL(TOKEN_END, tl.tokens[1].type);
}

TEST(TokenizerBasic, decimal_number) {
  TokenList tl = tokenize("3.14");
  LONGS_EQUAL(EXPR_OK, tl.error);
  LONGS_EQUAL(TOKEN_NUMBER, tl.tokens[0].type);
  DOUBLES_EQUAL(3.14, tl.tokens[0].value, 0.001);
}

TEST(TokenizerBasic, simple_expression) {
  TokenList tl = tokenize("1 + 2");
  LONGS_EQUAL(EXPR_OK, tl.error);
  LONGS_EQUAL(4, tl.count);
  LONGS_EQUAL(TOKEN_NUMBER, tl.tokens[0].type);
  LONGS_EQUAL(TOKEN_PLUS, tl.tokens[1].type);
  LONGS_EQUAL(TOKEN_NUMBER, tl.tokens[2].type);
  LONGS_EQUAL(TOKEN_END, tl.tokens[3].type);
}

TEST(TokenizerBasic, all_operators) {
  TokenList tl = tokenize("1+2-3*4/5");
  LONGS_EQUAL(EXPR_OK, tl.error);
  LONGS_EQUAL(10, tl.count);
  LONGS_EQUAL(TOKEN_PLUS, tl.tokens[1].type);
  LONGS_EQUAL(TOKEN_MINUS, tl.tokens[3].type);
  LONGS_EQUAL(TOKEN_STAR, tl.tokens[5].type);
  LONGS_EQUAL(TOKEN_SLASH, tl.tokens[7].type);
}

TEST_GROUP(TokenizerEdgeCases) { };

TEST(TokenizerEdgeCases, parentheses) {
  TokenList tl = tokenize("(1 + 2)");
  LONGS_EQUAL(EXPR_OK, tl.error);
  LONGS_EQUAL(TOKEN_LPAREN, tl.tokens[0].type);
  LONGS_EQUAL(TOKEN_RPAREN, tl.tokens[4].type);
}

TEST(TokenizerEdgeCases, whitespace_handling) {
  TokenList tl = tokenize("  1  +  2  ");
  LONGS_EQUAL(EXPR_OK, tl.error);
  LONGS_EQUAL(4, tl.count);
}

TEST(TokenizerEdgeCases, invalid_character) {
  TokenList tl = tokenize("1 + @");
  LONGS_EQUAL(EXPR_ERROR_INVALID_CHAR, tl.error);
  LONGS_EQUAL(4, tl.error_pos);
}

TEST(TokenizerEdgeCases, position_tracking) {
  TokenList tl = tokenize("12 + 34");
  LONGS_EQUAL(0, tl.tokens[0].pos);
  LONGS_EQUAL(3, tl.tokens[1].pos);
  LONGS_EQUAL(5, tl.tokens[2].pos);
}

int main(int ac, char** av) {
  return CommandLineTestRunner::RunAllTests(ac, av);
}
