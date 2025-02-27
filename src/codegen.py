class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.bytecode = []

    def generate_bytecode(self):
        self.walk(self.ast)
        return self.bytecode

    def walk(self, node):
        if node.type == "NUMBER":
            self.bytecode.append(f"PUSH {node.value}")
        elif node.type == "IDENT":
            self.bytecode.append(f"LOAD {node.value}")
        elif node.type == "ASSIGN":
            self.walk(node.children[1])
            self.bytecode.append(f"STORE {node.children[0].value}")
        elif node.type in ("PLUS", "MINUS", "MUL", "DIV"):
            self.walk(node.children[0])
            self.walk(node.children[1])
            self.bytecode.append(f"{node.type}")
