from backend.save_temp import save_temp_code
from backend.code_quality import pylint_score, complexity_analysis, maintainability_index

code = """
def add(a, b):
    return a + b

def calculate(a, b):
    if a > b:
        return a - b
    for i in range(5):
        print(i)
    return a * b
"""

# Step 1: Save code to temp file
temp_file = save_temp_code(code)

# Step 2: Run pylint
print("=== PYLINT SCORE ===")
print(pylint_score(temp_file))

# Step 3: Complexity
print("=== COMPLEXITY ===")
print(complexity_analysis(code))

# Step 4: Maintainability Index
print("=== MI SCORE ===")
print(maintainability_index(code))
