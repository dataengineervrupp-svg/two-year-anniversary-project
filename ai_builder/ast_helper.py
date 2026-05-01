import ast
from pathlib import Path
def is_constant_name(name: str) -> bool:
    return name.isupper()


def extract_python_symbols(file_path: Path) -> dict:
    """
    Extract top-level symbols from a Python file using ast.
    """
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    symbols = {
        "classes": [],
        "functions": [],
        "constants": [],
        "imports": [],
        "dataclass_fields": {},
    }

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                symbols["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imported_names = [alias.name for alias in node.names]
            symbols["imports"].append(
                f"from {module} import {', '.join(imported_names)}"
            )

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and is_constant_name(target.id):
                    symbols["constants"].append(target.id)

        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and is_constant_name(node.target.id):
                symbols["constants"].append(node.target.id)

        elif isinstance(node, ast.FunctionDef):
            symbols["functions"].append(node.name)

        elif isinstance(node, ast.ClassDef):
            symbols["classes"].append(node.name)

            is_dataclass = any(
                (
                    isinstance(decorator, ast.Name)
                    and decorator.id == "dataclass"
                )
                or (
                    isinstance(decorator, ast.Call)
                    and isinstance(decorator.func, ast.Name)
                    and decorator.func.id == "dataclass"
                )
                for decorator in node.decorator_list
            )

            if is_dataclass:
                fields = []

                for class_node in node.body:
                    if isinstance(class_node, ast.AnnAssign):
                        if isinstance(class_node.target, ast.Name):
                            fields.append(class_node.target.id)

                symbols["dataclass_fields"][node.name] = fields

    return symbols