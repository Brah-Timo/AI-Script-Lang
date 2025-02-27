class Debugger:
    def __init__(self, vm):
        self.vm = vm
        self.breakpoints = set()
        self.current_index = 0

    def set_breakpoint(self, index):
        self.breakpoints.add(index)
        print(f"🔴 Breakpoint set at instruction {index}")

    def print_stack(self):
        print("🛠 Stack:", self.vm.stack)

    def print_variables(self):
        print("📦 Variables:", self.vm.variables)

    def start(self):
        print("🔍 Starting Debugger...")
        while self.current_index < len(self.vm.bytecode):
            instr = self.vm.bytecode[self.current_index]

            if self.current_index in self.breakpoints:
                print(f"\n⏸ Paused at instruction {self.current_index}: {instr}")
                self.debug_prompt()

            self.execute_instruction(instr)
            self.current_index += 1

        print("✅ Execution finished.")

    def execute_instruction(self, instruction):
        parts = instruction.split()
        if parts[0] == "PUSH":
            self.vm.stack.append(float(parts[1]))
        elif parts[0] in ("PLUS", "MINUS", "MUL", "DIV"):
            b, a = self.vm.stack.pop(), self.vm.stack.pop()
            if parts[0] == "PLUS":
                self.vm.stack.append(a + b)
            elif parts[0] == "MINUS":
                self.vm.stack.append(a - b)
            elif parts[0] == "MUL":
                self.vm.stack.append(a * b)
            elif parts[0] == "DIV":
                if b == 0:
                    raise ZeroDivisionError("Division by zero error")
                self.vm.stack.append(a / b)
        elif parts[0] == "ASSIGN":
            var_name = parts[1]
            self.vm.variables[var_name] = self.vm.stack.pop()
        elif parts[0] == "LOAD":
            var_name = parts[1]
            if var_name in self.vm.variables:
                self.vm.stack.append(self.vm.variables[var_name])
            else:
                raise NameError(f"Variable '{var_name}' not defined")
        elif parts[0] == "PRINT":
            print("🖨 Output:", self.vm.stack.pop())

    def debug_prompt(self):
        while True:
            command = input("(debugger) ").strip().lower()
            if command == "step":
                break
            elif command == "continue":
                self.breakpoints.clear()
                break
            elif command == "print_stack":
                self.print_stack()
            elif command == "print_vars":
                self.print_variables()
            elif command.startswith("break "):
                _, index = command.split()
                self.set_breakpoint(int(index))
            else:
                print("⚠ Unknown command. Available commands: step, continue, print_stack, print_vars, break <index>")
