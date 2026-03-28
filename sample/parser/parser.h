#ifndef EXPR_PARSER_H_
#define EXPR_PARSER_H_

#include "error.h"
#include "tokenizer.h"

typedef enum {
  NODE_NUMBER,
  NODE_UNARY_MINUS,
  NODE_ADD,
  NODE_SUB,
  NODE_MUL,
  NODE_DIV
} NodeType;

typedef struct ASTNode ASTNode;

struct ASTNode {
  NodeType type;
  double value;      /* valid when type == NODE_NUMBER */
  ASTNode *left;     /* operand for unary; left operand for binary */
  ASTNode *right;    /* right operand for binary; NULL otherwise */
};

#define MAX_NODES 256

typedef struct {
  ASTNode nodes[MAX_NODES];
  int count;
  ASTNode *root;
  ExprError error;
  int error_pos;
} ParseResult;

/* Parse a token list into an AST.
   On success, error == EXPR_OK and root points to the AST root.
   On failure, error is set and error_pos indicates the position. */
ParseResult parse(const TokenList *tokens);

#endif /* EXPR_PARSER_H_ */
