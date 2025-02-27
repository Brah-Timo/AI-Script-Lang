import sys
import time
from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator
from vm import VirtualMachine
from debugger import Debugger

def compile_and_run(filename, debug=False, verbose=False):
    try:
        with open(filename, 'r') as file:
            source_code = file.read()

        if verbose:
            print("📜 Loading source file...\n")

        # 🔹 التحليل اللغوي
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        if verbose:
            print("🔍 Tokens:", tokens, "\n")

        # 🔹 التحليل النحوي
        parser = Parser(tokens)
        ast = parser.parse()

        if verbose:
            print("🌲 AST:", ast, "\n")

        # 🔹 توليد الـ Bytecode
        codegen = CodeGenerator(ast)
        bytecode = codegen.generate_bytecode()

        if verbose:
            print("⚙️ Bytecode:", bytecode, "\n")

        # 🔹 تنفيذ الكود الافتراضي مع قياس الأداء
        vm = VirtualMachine(bytecode)
        start_time = time.time()
        vm.execute()
        execution_time = time.time() - start_time

        print(f"⏱ Execution Time: {execution_time:.5f} seconds")

        # 🔹 التصحيح إن كان مفعّلًا
        if debug:
            print("\n🐞 Debugging Mode Activated...\n")
            debugger = Debugger(vm)
            debugger.start()

    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
    except SyntaxError as e:
        print(f"⚠️ Syntax Error: {e}")
    except Exception as e:
        print(f"🚨 Unexpected Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file.ai> [--debug] [--verbose]")
        sys.exit(1)

    source_file = sys.argv[1]
    debug_mode = "--debug" in sys.argv
    verbose_mode = "--verbose" in sys.argv

    compile_and_run(source_file, debug_mode, verbose_mode)
