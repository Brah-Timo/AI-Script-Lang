import unittest
from codegen import CodeGenerator
from parser import ASTNode

class TestCodeGen(unittest.TestCase):
    
    def setUp(self):
        """تحضير كائن مولد الكود قبل كل اختبار."""
        self.codegen = CodeGenerator()

    def test_generate_assignment(self):
        """اختبار توليد كود IR لتعبير تعيين متغير."""
        ast = ASTNode("ASSIGN", None, [ASTNode("IDENT", "x"), ASTNode("NUMBER", "10")])
        ir_code = self.codegen.generate(ast)
        self.assertEqual(ir_code, "x = 10", "خطأ في توليد تعبير التعيين!")

    def test_generate_addition(self):
        """اختبار توليد كود IR لعملية الجمع."""
        ast = ASTNode("ADD", None, [ASTNode("NUMBER", "5"), ASTNode("NUMBER", "3")])
        ir_code = self.codegen.generate(ast)
        self.assertEqual(ir_code, "5 + 3", "خطأ في توليد تعبير الجمع!")

    def test_generate_subtraction(self):
        """اختبار توليد كود IR لعملية الطرح."""
        ast = ASTNode("SUB", None, [ASTNode("NUMBER", "8"), ASTNode("NUMBER", "2")])
        ir_code = self.codegen.generate(ast)
        self.assertEqual(ir_code, "8 - 2", "خطأ في توليد تعبير الطرح!")

    def test_generate_complex_expression(self):
        """اختبار توليد كود IR لتعبير رياضي معقد."""
        ast = ASTNode("ASSIGN", None, [
            ASTNode("IDENT", "y"),
            ASTNode("ADD", None, [
                ASTNode("NUMBER", "4"),
                ASTNode("SUB", None, [
                    ASTNode("NUMBER", "10"),
                    ASTNode("NUMBER", "3")
                ])
            ])
        ])
        ir_code = self.codegen.generate(ast)
        self.assertTrue("y = 4 + (10 - 3)" in ir_code, "خطأ في توليد التعبير المعقد!")

if __name__ == "__main__":
    unittest.main()
