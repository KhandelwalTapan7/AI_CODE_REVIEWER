import ast

def analyze_code(code):
    tree = ast.parse(code)
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Detect empty function body
            if len(node.body) == 0:
                issues.append(f"Function '{node.name}' is empty.")

            # Detect function with only 'pass'
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                issues.append(f"Function '{node.name}' contains only 'pass'. Add implementation.")

        if isinstance(node, ast.Import):
            for name in node.names:
                issues.append(f"Import detected: {name.name}")

    return issues

print(analyze_code("def f(): pass"))
