import unittest
from lexer import Lexer

class TestLexer(unittest.TestCase):
    
    def setUp(self):
        """تحضير كائن Lexer قبل كل اختبار."""
        self.lexer = None  

    def tokenize_and_compare(self, code, expected_tokens):
        """اختبار عملية تحويل الكود إلى توكنات ومقارنتها مع النتيجة المتوقعة."""
        self.lexer = Lexer(code)
        tokens = self.lexer.tokenize()
        self.assertEqual(tokens, expected_tokens, f"خطأ في تحليل الكود: {code}")

    def test_variable_declaration(self):
        """اختبار تحليل كود تعريف متغير."""
        code = "let x = 10;"
        expected = [
            ("KEYWORD", "let"), 
            ("IDENT", "x"), 
            ("ASSIGN", "="), 
            ("NUMBER", "10"), 
            ("SEMICOLON", ";")
        ]
        self.tokenize_and_compare(code, expected)

    def test_if_statement(self):
        """اختبار تحليل جملة شرطية `if`."""
        code = "if (x > 5) { y = x + 1; }"
        expected = [
            ("KEYWORD", "if"), 
            ("LPAREN", "("), 
            ("IDENT", "x"), 
            ("GT", ">"), 
            ("NUMBER", "5"), 
            ("RPAREN", ")"), 
            ("LBRACE", "{"), 
            ("IDENT", "y"), 
            ("ASSIGN", "="), 
            ("IDENT", "x"), 
            ("PLUS", "+"), 
            ("NUMBER", "1"), 
            ("SEMICOLON", ";"), 
            ("RBRACE", "}")
        ]
        self.tokenize_and_compare(code, expected)

    def test_while_loop(self):
        """اختبار تحليل جملة `while`."""
        code = "while (count < 10) { count = count + 1; }"
        expected = [
            ("KEYWORD", "while"), 
            ("LPAREN", "("), 
            ("IDENT", "count"), 
            ("LT", "<"), 
            ("NUMBER", "10"), 
            ("RPAREN", ")"), 
            ("LBRACE", "{"), 
            ("IDENT", "count"), 
            ("ASSIGN", "="), 
            ("IDENT", "count"), 
            ("PLUS", "+"), 
            ("NUMBER", "1"), 
            ("SEMICOLON", ";"), 
            ("RBRACE", "}")
        ]
        self.tokenize_and_compare(code, expected)

    def test_function_definition(self):
        """اختبار تحليل تعريف دالة."""
        code = "function add(a, b) { return a + b; }"
        expected = [
            ("KEYWORD", "function"), 
            ("IDENT", "add"), 
            ("LPAREN", "("), 
            ("IDENT", "a"), 
            ("COMMA", ","), 
            ("IDENT", "b"), 
            ("RPAREN", ")"), 
            ("LBRACE", "{"), 
            ("KEYWORD", "return"), 
            ("IDENT", "a"), 
            ("PLUS", "+"), 
            ("IDENT", "b"), 
            ("SEMICOLON", ";"), 
            ("RBRACE", "}")
        ]
        self.tokenize_and_compare(code, expected)

    def test_single_line_comment(self):
        """اختبار تحليل تعليق سطري."""
        code = "// هذا تعليق"
        expected = [("COMMENT", "// هذا تعليق")]
        self.tokenize_and_compare(code, expected)

    def test_multi_line_comment(self):
        """اختبار تحليل تعليق متعدد الأسطر."""
        code = "/* تعليق\nمتعدد\nالأسطر */"
        expected = [("COMMENT", "/* تعليق\nمتعدد\nالأسطر */")]
        self.tokenize_and_compare(code, expected)

if __name__ == "__main__":
    unittest.main()
