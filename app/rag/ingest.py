from sqlalchemy.orm import Session

from app.models import Chunk, Document
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vectorstore import upsert_chunks
from app.schemas import IngestRequest


def ingest_document(db: Session, payload: IngestRequest) -> Document:
    document = Document(
        source_type=payload.source_type,
        source_name=payload.source_name,
        content=payload.content,
        extra_metadata=payload.extra_metadata,
    )
    db.add(document)
    db.flush()

    texts = chunk_text(payload.content)
    if not texts:
        db.commit()
        db.refresh(document)
        return document

    chunks = [
        Chunk(document_id=document.id, chunk_index=index, content=text)
        for index, text in enumerate(texts)
    ]
    db.add_all(chunks)
    db.flush()

    vectors = embed_texts(texts)
    upsert_chunks(
        chunk_ids=[chunk.id for chunk in chunks],
        vectors=vectors,
        payloads=[
            {
                "chunk_id": str(chunk.id),
                "document_id": str(document.id),
                "source_type": document.source_type,
                "source_name": document.source_name,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "extra_metadata": document.extra_metadata,
            }
            for chunk in chunks
        ],
    )
    db.commit()
    db.refresh(document)
    return document
