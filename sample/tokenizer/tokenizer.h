#ifndef EXPR_TOKENIZER_H_
#define EXPR_TOKENIZER_H_

#include "error.h"

typedef enum {
  TOKEN_NUMBER,
  TOKEN_PLUS,
  TOKEN_MINUS,
  TOKEN_STAR,
  TOKEN_SLASH,
  TOKEN_LPAREN,
  TOKEN_RPAREN,
  TOKEN_END,
  TOKEN_ERROR
} TokenType;

typedef struct {
  TokenType type;
  double value;    /* valid when type == TOKEN_NUMBER */
  int pos;         /* position in input string */
} Token;

#define MAX_TOKENS 256

typedef struct {
  Token tokens[MAX_TOKENS];
  int count;
  ExprError error;
  int error_pos;
} TokenList;

/* Tokenize the input string. Returns a TokenList.
   On success, error == EXPR_OK and tokens ends with TOKEN_END.
   On failure, error is set and error_pos indicates the position. */
TokenList tokenize(const char *input);

#endif /* EXPR_TOKENIZER_H_ */
