class Optimizer:
    def __init__(self):
        pass

    def constant_folding(self, ast):
        """تطبيق تحسينات مثل تبسيط العمليات الحسابية الثابتة"""
        if ast.type in ("PLUS", "MINUS", "MUL", "DIV") and \
           ast.children[0].type == "NUMBER" and ast.children[1].type == "NUMBER":
            left_val = float(ast.children[0].value)
            right_val = float(ast.children[1].value)

            if ast.type == "PLUS":
                return ASTNode("NUMBER", str(left_val + right_val))
            elif ast.type == "MINUS":
                return ASTNode("NUMBER", str(left_val - right_val))
            elif ast.type == "MUL":
                return ASTNode("NUMBER", str(left_val * right_val))
            elif ast.type == "DIV":
                if right_val != 0:
                    return ASTNode("NUMBER", str(left_val / right_val))
                else:
                    raise ZeroDivisionError("تقسيم على الصفر غير مسموح")

        return ast

    def eliminate_dead_code(self, ast):
        """إزالة الأكواد غير الضرورية"""
        if ast.type == "ASSIGN" and ast.children[1].type == "NUMBER":
            val = float(ast.children[1].value)
            if val == 0:
                return None  # إزالة الأسطر غير الضرورية
            elif val == 1 and ast.children[0].type == "MUL":
                return ast.children[0]  # x * 1 يصبح x
            elif ast.children[0].type == "DIV" and val == 1:
                return ast.children[0]  # x / 1 يصبح x

        return ast

    def optimize(self, ast):
        """تطبيق جميع التحسينات على الشجرة بالكامل"""
        if ast is None:
            return None

        # تحسين الأبناء أولًا
        ast.children = [self.optimize(child) for child in ast.children if child]

        # تطبيق تحسينات فردية
        ast = self.constant_folding(ast)
        ast = self.eliminate_dead_code(ast)

        return ast

# ✅ مثال استخدام:
if __name__ == "__main__":
    from ast import ASTNode

    optimizer = Optimizer()
    
    expr = ASTNode("PLUS", "+", [ASTNode("NUMBER", "5"), ASTNode("NUMBER", "3")])
    optimized_expr = optimizer.optimize(expr)
    
    print("🔹 AST المحسن:", optimized_expr)
