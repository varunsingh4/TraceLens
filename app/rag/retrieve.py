from uuid import UUID

from app.rag.embeddings import embed_query
from app.rag.vectorstore import search
from app.schemas import RetrievedChunk


def retrieve_top_chunks(question: str, limit: int = 5) -> list[RetrievedChunk]:
    """Embed the question the same way we embed chunks, then ask Qdrant for nearest neighbors.

    Same embedding space is the whole trick: if we embedded documents with MiniLM
    and the question with a different model, scores would be meaningless.
    """
    query_vector = embed_query(question)
    hits = search(query_vector, limit=limit)
    results: list[RetrievedChunk] = []
    for rank, (score, payload) in enumerate(hits, start=1):
        results.append(
            RetrievedChunk(
                rank=rank,
                score=score,
                chunk_id=UUID(payload["chunk_id"]),
                document_id=UUID(payload["document_id"]),
                source_type=payload["source_type"],
                source_name=payload["source_name"],
                chunk_index=payload["chunk_index"],
                content=payload["content"],
                extra_metadata=payload.get("extra_metadata") or {},
            )
        )
    return results
