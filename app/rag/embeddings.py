from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import settings


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load the model once. First call downloads weights; later calls reuse RAM."""
    return SentenceTransformer(settings.embedding_model)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [vector.tolist() for vector in vectors]


def embed_query(question: str) -> list[float]:
    return embed_texts([question])[0]


def embedding_dimension() -> int:
    model = get_model()
    dimension = (
        model.get_embedding_dimension()
        if hasattr(model, "get_embedding_dimension")
        else model.get_sentence_embedding_dimension()
    )
    if dimension is None:
        raise RuntimeError(f"{settings.embedding_model} did not report a vector size.")
    return dimension

