from backend.embeddings import get_code_embedding

code1 = """
def add(a, b):
    return a + b
"""

code2 = """
def sum_numbers(x, y):
    return x + y
"""

e1 = get_code_embedding(code1)
e2 = get_code_embedding(code2)

print("Embedding 1 shape:", e1.shape)
print("Embedding 2 shape:", e2.shape)
