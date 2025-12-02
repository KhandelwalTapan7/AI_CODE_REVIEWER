import subprocess
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def pylint_score(file_path):
    """Run pylint on a file and return output text"""
    result = subprocess.run(
        ["pylint", file_path, "--score=y", "--disable=R,C"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout


def complexity_analysis(code):
    """Return cyclomatic complexity for each function."""
    results = cc_visit(code)
    output = []
    for r in results:
        output.append(f"{r.name}: Complexity {r.complexity}")
    return output


def maintainability_index(code):
    """Return maintainability index score."""
    score = mi_visit(code, False)
    return score
