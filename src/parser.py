class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"ASTNode({self.type}, {self.value}, {self.children})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == token_type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        return None

    def parse(self):
        return self.statement()

    def statement(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == "IDENT":
            var_name = self.consume("IDENT")
            self.consume("ASSIGN")
            expr_node = self.expr()
            return ASTNode("ASSIGN", var_name.value, [expr_node])
        return self.expr()

    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type in ("PLUS", "MINUS"):
            op = self.tokens[self.pos]
            self.pos += 1
            node = ASTNode(op.type, op.value, [node, self.term()])
        return node

    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type in ("MUL", "DIV"):
            op = self.tokens[self.pos]
            self.pos += 1
            node = ASTNode(op.type, op.value, [node, self.factor()])
        return node

    def factor(self):
        token = self.tokens[self.pos]
        if token.type == "NUMBER":
            self.pos += 1
            return ASTNode("NUMBER", token.value)
        elif token.type == "LPAREN":
            self.pos += 1
            node = self.expr()
            self.consume("RPAREN")
            return node
        elif token.type == "IDENT":
            self.pos += 1
            return ASTNode("IDENT", token.value)
        raise SyntaxError("Invalid syntax")
