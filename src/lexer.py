import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.token_specs = [
            ("NUMBER", r"\d+(\.\d*)?"),  # أرقام صحيحة وعشرية
            ("IDENT", r"[a-zA-Z_]\w*"),  # أسماء المتغيرات والدوال
            ("ASSIGN", r"="),  # إسناد
            ("PLUS", r"\+"),  # جمع
            ("MINUS", r"-"),  # طرح
            ("MUL", r"\*"),  # ضرب
            ("DIV", r"/"),  # قسمة
            ("LPAREN", r"\("),  # قوس مفتوح
            ("RPAREN", r"\)"),  # قوس مغلق
            ("LBRACE", r"\{"),  # قوس معقوف مفتوح
            ("RBRACE", r"\}"),  # قوس معقوف مغلق
            ("COMMA", r","),  # فاصلة
            ("SEMICOLON", r";"),  # فاصلة منقوطة
            ("NEWLINE", r"\n"),  # سطر جديد
            ("SKIP", r"[ \t]+"),  # تخطي المسافات البيضاء
            ("COMMENT", r"#.*"),  # التعليقات
            ("BOOL", r"\b(?:true|false)\b"),  # القيم المنطقية
            ("KEYWORD", r"\b(?:if|else|for|while|return|def|class)\b"),  # الكلمات المفتاحية
            ("STRING", r"\".*?\"|\'.*?\'"),  # النصوص بين علامات تنصيص
            ("ERROR", r".")  # أي رمز غير متوقع
        ]

    def tokenize(self):
        token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.token_specs)
        for match in re.finditer(token_regex, self.source_code):
            kind = match.lastgroup
            value = match.group()
            if kind == "SKIP" or kind == "COMMENT":
                continue  # تجاهل المسافات البيضاء والتعليقات
            elif kind == "ERROR":
                raise SyntaxError(f"Unexpected token: {value}")
            self.tokens.append(Token(kind, value))
        return self.tokens
