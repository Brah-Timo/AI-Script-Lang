# لغة البرمجة AI-Script - مترجم ومصحح

## 📝 مقدمة
AI-Script هي لغة برمجة مخصصة لتحويل الصور إلى فيديوهات بالذكاء الاصطناعي، مع دعم التحسينات المتقدمة مثل التسريع باستخدام GPU والبرمجة المتوازية.

## 🚀 الميزات
- **مترجم ومفسر** لتحليل وتنفيذ الكود
- **دعم GPU Acceleration** عبر CUDA/OpenCL
- **LLVM IR & JIT** لتسريع الأداء
- **دعم AI-based Video Processing** لإنشاء فيديوهات احترافية
- **مصحح أخطاء (Debugger) لمراجعة وتنقيح الأكواد**
## 🛠 الميزات الأساسية:
✅ **تحويل الصور إلى فيديو بالذكاء الاصطناعي**  
✅ **دعم GPU عبر CUDA / OpenCL**  
✅ **تنفيذ فوري عبر JIT Execution**  
✅ **تسريع باستخدام LLVM و WebAssembly**  
✅ **تحسين جودة الفيديو بـ Super Resolution**  
✅ **تحليل وتتبع الحركات بالذكاء الاصطناعي**  
✅ **دعم Cloud AI Processing لمعالجة الفيديوهات الضخمة**  

## 🛠️ متطلبات التشغيل
- Python 3.8 أو أحدث
- LLVM 13.0 أو أحدث
- CUDA / OpenCL (اختياري لدعم GPU)

## 📦 التثبيت
```bash
git clone https://github.com/yourusername/ai_video_language.git
cd ai_video_language
pip install -r requirements.txt

▶️ الاستخدام
from ai_video_language import Compiler

code = '''
image = load("input.jpg")
video = animate(image, duration=5)
save(video, "output.mp4")
'''

compiler = Compiler()
compiler.run(code)

▶️ الاستخدام
تشغيل الكود مباشرة

python main.py example1.ai

تشغيل المفسر التفاعلي (REPL)

python repl.py

تشغيل الاختبارات

pytest tests/

🖥️ هيكلة المشروع

ai-script-compiler/


🔧 تطوير المشروع

    تحليل الكود باستخدام Lexer و Parser
    تحويله إلى LLVM IR ثم إلى Bytecode
    تنفيذه عبر LLVM JIT أو WebAssembly
    استخدام AI Models لتحليل وتحريك الصور
---
إنشاء ai-debugger.exe باستخدام pyinstaller

📌 نستخدم pyinstaller لإنشاء ملف تنفيذي منفصل للمصحح.
🔧 الخطوات:

    تثبيت pyinstaller

pip install pyinstaller

إنشاء الملف التنفيذي ai-debugger.exe

    pyinstaller --onefile --name ai-debugger src/debugger.py

    سيتم إنشاء ai-debugger.exe داخل مجلد dist/
        قم بنقل الملف إلى المكان المناسب.

تجربة ai-debugger.exe
✅ تشغيل المصحح مع سكريبت AI

ai-debugger.exe example_script.ai

🔹 سيتوقف التنفيذ عند السطر 2 بسبب breakpoint!
🔹 اضغط Enter للمتابعة خطوة بخطوة.
💡 النتيجة النهائية

✅ مصحح أخطاء قوي (ai-debugger.exe) لمترجم ai-script-compiler
✅ يدعم step execution, breakpoints, وعرض السطور أثناء التنفيذ
✅ متوافق مع pyinstaller لإنشاء ملف تنفيذي مستقل

🚀 الآن يمكنك تتبع أخطاء السكريبتات بسهولة وتحسين أداء المترجم!


## 📄 **2. `requirements.txt` - المكتبات المطلوبة**  
```txt
llvmlite>=0.39.0
numpy>=1.21.0
torch>=1.10.0
pytest>=7.0.0
pycuda>=2021.1
