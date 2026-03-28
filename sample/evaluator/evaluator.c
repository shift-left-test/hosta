#include "evaluator.h"
#include "parser.h"
#include "tokenizer.h"
#include <stddef.h>

static ExprResult make_result(double value) {
  return (ExprResult){.value = value, .error = EXPR_OK, .error_pos = -1};
}

static ExprResult make_error(ExprError error) {
  return (ExprResult){.value = 0.0, .error = error, .error_pos = -1};
}

static ExprResult evaluate_binary(const ASTNode *node) {
  ExprResult left = evaluate(node->left);
  if (left.error != EXPR_OK) return left;
  ExprResult right = evaluate(node->right);
  if (right.error != EXPR_OK) return right;

  switch (node->type) {
    case NODE_ADD: return make_result(left.value + right.value);
    case NODE_SUB: return make_result(left.value - right.value);
    case NODE_MUL: return make_result(left.value * right.value);
    case NODE_DIV:
      if (right.value == 0.0) return make_error(EXPR_ERROR_DIVISION_BY_ZERO);
      return make_result(left.value / right.value);
    default:
      return make_error(EXPR_ERROR_UNEXPECTED_TOKEN);
  }
}

ExprResult evaluate(const struct ASTNode *node) {
  if (node == NULL) {
    return make_error(EXPR_ERROR_EMPTY_EXPRESSION);
  }

  switch (node->type) {
    case NODE_NUMBER:
      return make_result(node->value);

    case NODE_UNARY_MINUS: {
      ExprResult inner = evaluate(node->left);
      if (inner.error != EXPR_OK) return inner;
      return make_result(-inner.value);
    }

    case NODE_ADD:
    case NODE_SUB:
    case NODE_MUL:
    case NODE_DIV:
      return evaluate_binary(node);
  }

  return make_error(EXPR_ERROR_UNEXPECTED_TOKEN);
}

ExprResult evaluate_expression(const char *input) {
  TokenList tokens = tokenize(input);
  if (tokens.error != EXPR_OK) {
    return (ExprResult){.value = 0.0, .error = tokens.error, .error_pos = tokens.error_pos};
  }

  ParseResult pr = parse(&tokens);
  if (pr.error != EXPR_OK) {
    return (ExprResult){.value = 0.0, .error = pr.error, .error_pos = pr.error_pos};
  }

  return evaluate(pr.root);
}
