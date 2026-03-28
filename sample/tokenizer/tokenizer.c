#include "tokenizer.h"
#include <ctype.h>
#include <stdlib.h>

static void add_token(TokenList *list, TokenType type, double value, int pos) {
  if (list->count < MAX_TOKENS) {
    list->tokens[list->count].type = type;
    list->tokens[list->count].value = value;
    list->tokens[list->count].pos = pos;
    list->count++;
  }
}

TokenList tokenize(const char *input) {
  TokenList list = {.count = 0, .error = EXPR_OK, .error_pos = -1};
  int i = 0;

  while (input[i] != '\0') {
    if (isspace((unsigned char)input[i])) {
      i++;
      continue;
    }

    if (isdigit((unsigned char)input[i]) || input[i] == '.') {
      char *end;
      double value = strtod(&input[i], &end);
      int len = (int)(end - &input[i]);
      add_token(&list, TOKEN_NUMBER, value, i);
      i += len;
      continue;
    }

    switch (input[i]) {
      case '+': add_token(&list, TOKEN_PLUS, 0, i); break;
      case '-': add_token(&list, TOKEN_MINUS, 0, i); break;
      case '*': add_token(&list, TOKEN_STAR, 0, i); break;
      case '/': add_token(&list, TOKEN_SLASH, 0, i); break;
      case '(': add_token(&list, TOKEN_LPAREN, 0, i); break;
      case ')': add_token(&list, TOKEN_RPAREN, 0, i); break;
      default:
        list.error = EXPR_ERROR_INVALID_CHAR;
        list.error_pos = i;
        return list;
    }
    i++;
  }

  add_token(&list, TOKEN_END, 0, i);
  return list;
}
