from app.config import settings


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[str]:
    """Split a document into overlapping windows.

    Why chunks, not whole documents?
    Retrieval ranks *pieces* of text. A 4-page runbook would drown a one-line
    stack frame if we stored both as a single vector.

    Why overlap?
    A sentence that sits on a split boundary would otherwise be cut in half
    and fail to match either chunk. Overlap keeps that sentence in both.
    """
    size = chunk_size or settings.chunk_size
    overlap = overlap if overlap is not None else settings.chunk_overlap
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    if len(cleaned) <= size:
        return [cleaned]

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + size, len(cleaned))
        chunks.append(cleaned[start:end])
        if end == len(cleaned):
            break
        start = end - overlap
    return chunks
