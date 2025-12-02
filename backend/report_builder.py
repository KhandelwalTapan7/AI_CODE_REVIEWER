from backend.static_analysis import analyze_code
from backend.code_quality import pylint_score, complexity_analysis, maintainability_index
from backend.embeddings import get_code_embedding
from backend.save_temp import save_temp_code
from backend.llm_review import review_code_with_llm  # Ensure to import review_code_with_llm

import json

def generate_report(code: str):
    """Generates a complete analysis report for a piece of code."""

    # 1. Save code to a temp file for pylint
    temp_path = save_temp_code(code)

    # 2. Static analysis
    static_issues = analyze_code(code)

    # 3. Pylint score
    pylint_output = pylint_score(temp_path)

    # 4. Complexity
    complexity = complexity_analysis(code)

    # 5. Maintainability Index
    maintainability = maintainability_index(code)

    # 6. Embedding (vector representation of code)
    embedding_vector = get_code_embedding(code)
    embedding_vector = embedding_vector.tolist()  # convert numpy → list (JSON friendly)

    # 7. LLM Review (AI suggestions for bugs, security, performance, etc.)
    llm_review = review_code_with_llm(code)

    # 8. Prepare final report
    report = {
        "static_analysis": static_issues,
        "pylint_score": pylint_output,
        "complexity": complexity,
        "maintainability_index": maintainability,
        "embedding_vector_first_10_values": embedding_vector[:10],  # show only first values
        "full_embedding_length": len(embedding_vector),
        "llm_review": llm_review  # Add LLM review result here
    }

    return report


# Testing the pipeline
if __name__ == "__main__":
    sample_code = """
def add(a, b):
    return a + b

def calculate(x, y):
    if x > y:
        return x - y
    else:
        for i in range(5):
            print(i)
    return x * y
"""
    result = generate_report(sample_code)
    print(json.dumps(result, indent=4))
