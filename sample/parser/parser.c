#include "parser.h"
#include <stddef.h>

static ParseResult *current_result;
static const TokenList *current_tokens;
static int current_pos;

static ASTNode *alloc_node(NodeType type) {
  if (current_result->count >= MAX_NODES) {
    return NULL;
  }
  ASTNode *node = &current_result->nodes[current_result->count++];
  node->type = type;
  node->value = 0;
  node->left = NULL;
  node->right = NULL;
  return node;
}

static const Token *peek(void) {
  return &current_tokens->tokens[current_pos];
}

static const Token *advance(void) {
  return &current_tokens->tokens[current_pos++];
}

static ASTNode *parse_expression(void);

static ASTNode *parse_primary(void) {
  const Token *tok = peek();

  if (tok->type == TOKEN_NUMBER) {
    advance();
    ASTNode *node = alloc_node(NODE_NUMBER);
    node->value = tok->value;
    return node;
  }

  if (tok->type == TOKEN_LPAREN) {
    advance();
    ASTNode *node = parse_expression();
    if (node == NULL) {
      return NULL;
    }
    if (peek()->type != TOKEN_RPAREN) {
      current_result->error = EXPR_ERROR_MISSING_PAREN;
      current_result->error_pos = peek()->pos;
      return NULL;
    }
    advance();
    return node;
  }

  if (tok->type == TOKEN_END) {
    current_result->error = EXPR_ERROR_EMPTY_EXPRESSION;
    current_result->error_pos = tok->pos;
  } else {
    current_result->error = EXPR_ERROR_UNEXPECTED_TOKEN;
    current_result->error_pos = tok->pos;
  }
  return NULL;
}

static ASTNode *parse_unary(void) {
  if (peek()->type == TOKEN_MINUS) {
    advance();
    ASTNode *operand = parse_unary();
    if (operand == NULL) {
      return NULL;
    }
    ASTNode *node = alloc_node(NODE_UNARY_MINUS);
    node->left = operand;
    return node;
  }
  return parse_primary();
}

static ASTNode *parse_term(void) {
  ASTNode *left = parse_unary();
  if (left == NULL) {
    return NULL;
  }

  while (peek()->type == TOKEN_STAR || peek()->type == TOKEN_SLASH) {
    NodeType type = (peek()->type == TOKEN_STAR) ? NODE_MUL : NODE_DIV;
    advance();
    ASTNode *right = parse_unary();
    if (right == NULL) {
      return NULL;
    }
    ASTNode *node = alloc_node(type);
    node->left = left;
    node->right = right;
    left = node;
  }

  return left;
}

static ASTNode *parse_expression(void) {
  ASTNode *left = parse_term();
  if (left == NULL) {
    return NULL;
  }

  while (peek()->type == TOKEN_PLUS || peek()->type == TOKEN_MINUS) {
    NodeType type = (peek()->type == TOKEN_PLUS) ? NODE_ADD : NODE_SUB;
    advance();
    ASTNode *right = parse_term();
    if (right == NULL) {
      return NULL;
    }
    ASTNode *node = alloc_node(type);
    node->left = left;
    node->right = right;
    left = node;
  }

  return left;
}

ParseResult parse(const TokenList *tokens) {
  ParseResult result = {.count = 0, .root = NULL, .error = EXPR_OK, .error_pos = -1};

  if (tokens->error != EXPR_OK) {
    result.error = tokens->error;
    result.error_pos = tokens->error_pos;
    return result;
  }

  current_result = &result;
  current_tokens = tokens;
  current_pos = 0;

  result.root = parse_expression();

  if (result.error == EXPR_OK && result.root != NULL) {
    if (peek()->type != TOKEN_END) {
      result.error = EXPR_ERROR_UNEXPECTED_TOKEN;
      result.error_pos = peek()->pos;
      result.root = NULL;
    }
  }

  return result;
}
