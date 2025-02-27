import json

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"ASTNode({self.type}, {self.value}, {self.children})"

    def traverse(self, level=0):
        indent = "  " * level
        print(f"{indent}- Node Type: {self.type}, Value: {self.value}")
        for child in self.children:
            child.traverse(level + 1)

    def to_dict(self):
        """ تحويل الشجرة إلى صيغة JSON-friendly Dictionary """
        return {
            "type": self.type,
            "value": self.value,
            "children": [child.to_dict() for child in self.children]
        }

    def to_json(self, filename=None):
        """ تصدير شجرة AST إلى ملف JSON """
        json_data = json.dumps(self.to_dict(), indent=4)
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(json_data)
        return json_data
