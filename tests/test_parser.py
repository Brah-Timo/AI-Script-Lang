import unittest
from lexer import Lexer
from parser import Parser, ASTNode

class TestParser(unittest.TestCase):

    def parse_and_compare(self, code, expected_type, expected_values):
        """تحليل الكود ومقارنة العقد الرئيسية في شجرة `AST`."""
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        self.assertEqual(ast.type, expected_type, f"خطأ: النوع المتوقع {expected_type} ولكن تم العثور على {ast.type}")
        
        for i, expected_value in enumerate(expected_values):
            self.assertEqual(ast.children[i].value, expected_value, 
                             f"خطأ في العنصر {i}: القيمة المتوقعة {expected_value} ولكن تم العثور على {ast.children[i].value}")

    def test_parse_assignment(self):
        """اختبار تحليل عملية إسناد متغير."""
        code = "let x = 10;"
        self.parse_and_compare(code, "ASSIGN", ["x", "10"])

    def test_parse_if_statement(self):
        """اختبار تحليل جملة `if` الشرطية."""
        code = "if (x > 5) { y = 1; }"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()

        self.assertEqual(ast.type, "IF", "لم يتم تحليل جملة `if` بشكل صحيح")
        self.assertEqual(ast.children[0].type, "CONDITION", "لم يتم تحليل الشرط داخل `if`")
        self.assertEqual(ast.children[1].type, "BLOCK", "لم يتم تحليل الجسم `{}` بشكل صحيح")

    def test_parse_while_loop(self):
        """اختبار تحليل جملة `while`."""
        code = "while (x < 10) { x = x + 1; }"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()

        self.assertEqual(ast.type, "WHILE", "لم يتم التعرف على `while`")
        self.assertEqual(ast.children[0].type, "CONDITION", "لم يتم تحليل شرط `while`")
        self.assertEqual(ast.children[1].type, "BLOCK", "لم يتم تحليل جسم `while`")

    def test_parse_function_definition(self):
        """اختبار تحليل تعريف دالة."""
        code = "function add(a, b) { return a + b; }"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()

        self.assertEqual(ast.type, "FUNCTION", "لم يتم التعرف على `function`")
        self.assertEqual(ast.children[0].value, "add", "خطأ في اسم الدالة")
        self.assertEqual(ast.children[1].type, "PARAMS", "خطأ في تحليل المعاملات")
        self.assertEqual(ast.children[2].type, "BLOCK", "لم يتم تحليل جسم الدالة")

    def test_parse_expression(self):
        """اختبار تحليل تعبير حسابي."""
        code = "result = (x + y) * 2;"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()

        self.assertEqual(ast.type, "ASSIGN", "لم يتم التعرف على الإسناد")
        self.assertEqual(ast.children[0].value, "result", "خطأ في المتغير المستهدف")
        self.assertEqual(ast.children[1].type, "EXPRESSION", "لم يتم تحليل التعبير الحسابي")

if __name__ == "__main__":
    unittest.main()
