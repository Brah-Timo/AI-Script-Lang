import unittest
from vm import VirtualMachine

class TestVM(unittest.TestCase):

    def setUp(self):
        """تحضير بيئة الاختبار وإنشاء كائن VirtualMachine جديد لكل اختبار."""
        self.vm = VirtualMachine()

    def test_execution_basic(self):
        """اختبار تنفيذ تعليمات أساسية مثل PUSH, STORE, LOAD, PRINT."""
        bytecode = [("PUSH", 10), ("STORE", "x"), ("LOAD", "x"), ("PRINT",)]
        output = self.vm.execute(bytecode)
        self.assertEqual(output, "10", "القيمة المطبوعة غير صحيحة")

    def test_execution_arithmetic(self):
        """اختبار العمليات الحسابية الأساسية ADD, SUB, MUL, DIV."""
        bytecode = [
            ("PUSH", 10), 
            ("PUSH", 5), 
            ("ADD",), 
            ("PRINT",)
        ]
        output = self.vm.execute(bytecode)
        self.assertEqual(output, "15", "خطأ في عملية الجمع")

        bytecode = [
            ("PUSH", 10), 
            ("PUSH", 5), 
            ("SUB",), 
            ("PRINT",)
        ]
        output = self.vm.execute(bytecode)
        self.assertEqual(output, "5", "خطأ في عملية الطرح")

        bytecode = [
            ("PUSH", 10), 
            ("PUSH", 5), 
            ("MUL",), 
            ("PRINT",)
        ]
        output = self.vm.execute(bytecode)
        self.assertEqual(output, "50", "خطأ في عملية الضرب")

        bytecode = [
            ("PUSH", 10), 
            ("PUSH", 2), 
            ("DIV",), 
            ("PRINT",)
        ]
        output = self.vm.execute(bytecode)
        self.assertEqual(output, "5", "خطأ في عملية القسمة")

    def test_execution_jump(self):
        """اختبار تعليمات التحكم في التدفق مثل JUMP و IF."""
        bytecode = [
            ("PUSH", 1),
            ("JUMP_IF_ZERO", 4),
            ("PUSH", "executed"),
            ("PRINT",)
        ]
        output = self.vm.execute(bytecode)
        self.assertEqual(output, "executed", "لم يتم تنفيذ القفزة بشكل صحيح")

    def test_execution_function_call(self):
        """اختبار تنفيذ الدوال عبر CALL و RETURN."""
        bytecode = [
            ("DEFINE_FUNC", "double", [
                ("LOAD", "x"),
                ("PUSH", 2),
                ("MUL",),
                ("RETURN",)
            ]),
            ("PUSH", 5),
            ("STORE", "x"),
            ("CALL", "double"),
            ("PRINT",)
        ]
        output = self.vm.execute(bytecode)
        self.assertEqual(output, "10", "خطأ في تنفيذ الدالة")

if __name__ == "__main__":
    unittest.main()
