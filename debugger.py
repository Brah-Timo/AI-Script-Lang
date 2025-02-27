import sys
import time
from src.compiler import Compiler  # تأكد من استيراد المترجم الأساسي

class Debugger:
    def __init__(self, script_path):
        self.script_path = script_path
        self.breakpoints = set()
        self.current_line = 0
        self.running = True

    def load_script(self):
        with open(self.script_path, "r") as file:
            self.lines = file.readlines()

    def set_breakpoint(self, line_num):
        self.breakpoints.add(line_num)

    def step(self):
        """تنفيذ سطر واحد من الشيفرة"""
        if self.current_line < len(self.lines):
            print(f"[DEBUG] Running line {self.current_line + 1}: {self.lines[self.current_line].strip()}")
            Compiler().execute_line(self.lines[self.current_line])  # تنفيذ السطر الحالي
            self.current_line += 1
        else:
            print("[DEBUG] Execution finished.")
            self.running = False

    def run(self):
        """تنفيذ البرنامج مع إمكانية التوقف عند نقاط التوقف"""
        print("[DEBUG] Starting execution...")
        self.load_script()

        while self.running and self.current_line < len(self.lines):
            if self.current_line + 1 in self.breakpoints:
                print(f"[DEBUG] Breakpoint hit at line {self.current_line + 1}. Press Enter to continue...")
                input()  # ينتظر إدخال المستخدم

            self.step()
            time.sleep(0.5)  # تأخير صغير لتوضيح التنفيذ التدريجي

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ai-debugger.py <script.ai>")
        sys.exit(1)

    debugger = Debugger(sys.argv[1])

    # إضافة نقطة توقف تجريبية عند السطر 2
    debugger.set_breakpoint(2)

    debugger.run()
