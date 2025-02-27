class VirtualMachine:
    def __init__(self, bytecode):
        self.bytecode = bytecode
        self.stack = []
        self.variables = {}  # لتخزين المتغيرات

    def execute(self):
        for instruction in self.bytecode:
            parts = instruction.split()

            if parts[0] == "PUSH":
                self.stack.append(float(parts[1]))

            elif parts[0] in ("PLUS", "MINUS", "MUL", "DIV"):
                b, a = self.stack.pop(), self.stack.pop()
                if parts[0] == "PLUS":
                    self.stack.append(a + b)
                elif parts[0] == "MINUS":
                    self.stack.append(a - b)
                elif parts[0] == "MUL":
                    self.stack.append(a * b)
                elif parts[0] == "DIV":
                    if b == 0:
                        raise ZeroDivisionError("Division by zero error")
                    self.stack.append(a / b)

            elif parts[0] == "ASSIGN":
                var_name = parts[1]
                self.variables[var_name] = self.stack.pop()

            elif parts[0] == "LOAD":
                var_name = parts[1]
                if var_name in self.variables:
                    self.stack.append(self.variables[var_name])
                else:
                    raise NameError(f"Variable '{var_name}' not defined")

            elif parts[0] == "PRINT":
                print("Output:", self.stack.pop())

        if self.stack:
            print("Final Result:", self.stack[-1])
