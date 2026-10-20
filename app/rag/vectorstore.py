from uuid import UUID

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from app.config import settings
from app.rag.embeddings import embedding_dimension

_client: QdrantClient | None = None


def get_qdrant() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=settings.qdrant_url)
    return _client


def ensure_collection() -> None:
    """Qdrant needs a collection with a fixed vector size before we upsert."""
    client = get_qdrant()
    existing = {c.name for c in client.get_collections().collections}
    if settings.qdrant_collection in existing:
        return
    client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(size=embedding_dimension(), distance=Distance.COSINE),
    )


def upsert_chunks(
    chunk_ids: list[UUID],
    vectors: list[list[float]],
    payloads: list[dict],
) -> None:
    ensure_collection()
    points = [
        PointStruct(id=str(chunk_id), vector=vector, payload=payload)
        for chunk_id, vector, payload in zip(chunk_ids, vectors, payloads, strict=True)
    ]
    get_qdrant().upsert(collection_name=settings.qdrant_collection, points=points)


def search(vector: list[float], limit: int = 5) -> list[tuple[float, dict]]:
    ensure_collection()
    hits = get_qdrant().search(
        collection_name=settings.qdrant_collection,
        query_vector=vector,
        limit=limit,
        with_payload=True,
    )
    return [(hit.score, hit.payload or {}) for hit in hits]
