#include <stdio.h>
#include <string.h>
#include "evaluator.h"

static const char *error_message(ExprError err) {
  switch (err) {
    case EXPR_OK:                    return "OK";
    case EXPR_ERROR_INVALID_CHAR:    return "invalid character";
    case EXPR_ERROR_UNEXPECTED_TOKEN: return "unexpected token";
    case EXPR_ERROR_MISSING_PAREN:   return "missing closing parenthesis";
    case EXPR_ERROR_EMPTY_EXPRESSION: return "empty expression";
    case EXPR_ERROR_DIVISION_BY_ZERO: return "division by zero";
  }
  return "unknown error";
}

int main(void) {
  char line[1024];

  printf("Expression Calculator\n");
  printf("Type an expression (e.g., 1 + 2 * (3 - 4)) or 'q' to quit.\n\n");

  while (1) {
    printf("> ");
    if (fgets(line, sizeof(line), stdin) == NULL) {
      break;
    }

    size_t len = strlen(line);
    if (len > 0 && line[len - 1] == '\n') {
      line[len - 1] = '\0';
    }

    if (strcmp(line, "q") == 0 || strcmp(line, "quit") == 0) {
      break;
    }

    ExprResult result = evaluate_expression(line);
    if (result.error == EXPR_OK) {
      printf("= %g\n\n", result.value);
    } else {
      printf("Error: %s", error_message(result.error));
      if (result.error_pos >= 0) {
        printf(" at position %d", result.error_pos);
      }
      printf("\n\n");
    }
  }

  return 0;
}
