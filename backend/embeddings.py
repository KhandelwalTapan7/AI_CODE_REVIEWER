from sentence_transformers import SentenceTransformer

# Load a model specialized for code
model = SentenceTransformer("microsoft/codebert-base")

def get_code_embedding(code: str):
    """Returns a vector embedding for the input code."""
    embedding = model.encode(code)
    return embedding
