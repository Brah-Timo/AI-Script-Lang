import llvmlite.binding as llvm
import llvmlite.ir as ir

class JITCompiler:
    def __init__(self):
        # تهيئة LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        self.target_machine = llvm.Target.from_default_triple().create_target_machine()
        self.execution_engine = self._create_execution_engine()

    def _create_execution_engine(self):
        """ إنشاء محرك تنفيذ JIT باستخدام MCJIT """
        backing_mod = llvm.parse_assembly("")
        engine = llvm.create_mcjit_compiler(backing_mod, self.target_machine)
        return engine

    def compile_ir(self, ir_code):
        """ ترجمة كود LLVM IR إلى كود قابل للتنفيذ """
        mod = llvm.parse_assembly(ir_code)
        mod.verify()
        self.execution_engine.add_module(mod)
        self.execution_engine.finalize_object()
        self.execution_engine.run_static_constructors()
        return self.execution_engine

    def execute_function(self, func_name):
        """ تنفيذ دالة JIT مترجمة واسترجاع النتيجة """
        func_ptr = self.execution_engine.get_function_address(func_name)
        import ctypes
        cfunc = ctypes.CFUNCTYPE(ctypes.c_int)(func_ptr)
        return cfunc()

# مثال استخدام:
if __name__ == "__main__":
    jit = JITCompiler()

    test_ir = """
    define i32 @main() {
    entry:
        ret i32 42
    }
    """

    jit.compile_ir(test_ir)
    result = jit.execute_function("main")
    print("🔹 JIT Execution Result:", result)
