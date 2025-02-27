class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"ASTNode({self.type}, {self.value}, {self.children})"

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # جدول الرموز لحفظ المتغيرات وأنواعها

    def analyze(self, ast):
        """تحليل المعنى والتحقق من الأخطاء المنطقية"""
        if ast.type == "ASSIGN":
            var_name = ast.children[0].value
            var_value = ast.children[1]
            
            if var_name in self.symbol_table:
                existing_type = self.symbol_table[var_name]['type']
                new_type = self.get_type(var_value)
                if existing_type != new_type:
                    raise TypeError(f"Type mismatch: {var_name} was {existing_type} but assigned {new_type}")

            self.symbol_table[var_name] = {'value': var_value.value, 'type': self.get_type(var_value)}

        elif ast.type == "IDENT":
            if ast.value not in self.symbol_table:
                raise NameError(f"Undefined variable: {ast.value}")

        elif ast.type in ("PLUS", "MINUS", "MUL", "DIV"):
            left, right = ast.children
            self.analyze(left)
            self.analyze(right)

            left_type = self.get_type(left)
            right_type = self.get_type(right)
            if left_type != right_type:
                raise TypeError(f"Type mismatch in operation: {left_type} {ast.type} {right_type}")

    def get_type(self, node):
        """تحديد نوع البيانات بناءً على العقدة"""
        if node.type == "NUMBER":
            return "int" if node.value.isdigit() else "float"
        elif node.type == "IDENT":
            return self.symbol_table.get(node.value, {}).get('type', "unknown")
        return "unknown"

# ✅ مثال استخدام:
if __name__ == "__main__":
    analyzer = SemanticAnalyzer()
    
    # تعيين متغير عددي
    assign_ast = ASTNode("ASSIGN", None, [ASTNode("IDENT", "x"), ASTNode("NUMBER", "10")])
    analyzer.analyze(assign_ast)

    # عملية رياضية على x
    expr_ast = ASTNode("PLUS", "+", [ASTNode("IDENT", "x"), ASTNode("NUMBER", "5")])
    analyzer.analyze(expr_ast)

    print("✅ Semantic Analysis Passed!")
