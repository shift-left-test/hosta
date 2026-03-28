#ifndef EXPR_EVALUATOR_H_
#define EXPR_EVALUATOR_H_

#include "error.h"

struct ASTNode;

/* Evaluate an AST tree and return the result. */
ExprResult evaluate(const struct ASTNode *node);

/* Convenience: tokenize + parse + evaluate a string expression in one call. */
ExprResult evaluate_expression(const char *input);

#endif /* EXPR_EVALUATOR_H_ */
