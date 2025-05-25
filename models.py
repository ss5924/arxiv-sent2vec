from sentence_transformers import SentenceTransformer


def load_model(model_name: str, device: str):
    return SentenceTransformer(model_name, device=device)
