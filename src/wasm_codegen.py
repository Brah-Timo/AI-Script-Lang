import subprocess

def compile_to_wasm(input_file, output_file, exported_functions=None, optimize=True):
    """
    تحويل كود C إلى WebAssembly باستخدام Emscripten.
    
    :param input_file: اسم ملف الإدخال (كود C)
    :param output_file: اسم ملف الإخراج (WASM)
    :param exported_functions: قائمة بالوظائف التي سيتم تصديرها إلى WebAssembly
    :param optimize: تفعيل تحسين الأداء
    """
    try:
        # إعداد الخيارات الافتراضية
        exported_funcs = exported_functions or ["_main"]
        exported_funcs_str = ",".join(f"'{func}'" for func in exported_funcs)

        # إعداد أوامر الترجمة
        cmd = [
            "emcc", input_file, "-o", output_file,
            "-s", f"EXPORTED_FUNCTIONS=[{exported_funcs_str}]",
            "-s", "EXPORTED_RUNTIME_METHODS=['cwrap','ccall']",
            "-s", "WASM=1"
        ]

        # إضافة تحسينات الأداء إذا تم التفعيل
        if optimize:
            cmd.append("-O3")

        # دعم `--no-entry` إذا لم يكن هناك دالة `main`
        if "_main" not in exported_funcs:
            cmd.append("--no-entry")

        # تنفيذ الأمر
        subprocess.run(cmd, check=True)
        print(f"✅ تم تحويل {input_file} بنجاح إلى {output_file}!")

    except subprocess.CalledProcessError as e:
        print(f"❌ فشل الترجمة! خطأ: {e}")

# ✅ تجربة تحويل كود C إلى WebAssembly
if __name__ == "__main__":
    compile_to_wasm("ai_script.c", "ai_script.wasm", exported_functions=["_process_data"])
