#ifndef EXPR_ERROR_H_
#define EXPR_ERROR_H_

typedef enum {
  EXPR_OK = 0,
  EXPR_ERROR_INVALID_CHAR,
  EXPR_ERROR_UNEXPECTED_TOKEN,
  EXPR_ERROR_MISSING_PAREN,
  EXPR_ERROR_EMPTY_EXPRESSION,
  EXPR_ERROR_DIVISION_BY_ZERO
} ExprError;

typedef struct {
  double value;
  ExprError error;
  int error_pos;
} ExprResult;

#endif /* EXPR_ERROR_H_ */
