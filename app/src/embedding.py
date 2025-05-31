from sentence_transformers import SentenceTransformer


def load_embedding_model(model_name: str = 'paraphrase-multilingual-mpnet-base-v2'):
    """
    Loads and returns a SentenceTransformer embedding model.
    """
    return SentenceTransformer(model_name)


def embed_texts(model, texts, show_progress_bar=True):
    """
    Generates embeddings for a list of texts using the provided model.
    Returns a list of embeddings (numpy arrays).
    """
    return model.encode(texts, show_progress_bar=show_progress_bar)