"""Load the sample evidence into TraceLens. Run: python -m app.seed"""

from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.rag.ingest import ingest_document
from app.rag.vectorstore import ensure_collection
from app.schemas import IngestRequest

SAMPLES = Path(__file__).resolve().parent.parent / "data" / "samples"


def main() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_collection()
    db = SessionLocal()
    try:
        for path in sorted(SAMPLES.iterdir()):
            if not path.is_file():
                continue
            source_type, source_name = path.stem.split("__", 1)
            payload = IngestRequest(
                source_type=source_type,
                source_name=source_name.replace("_", " "),
                content=path.read_text(),
                extra_metadata={"filename": path.name},
            )
            document = ingest_document(db, payload)
            print(f"ingested {path.name} -> {len(document.chunks)} chunks ({document.id})")
    finally:
        db.close()


if __name__ == "__main__":
    main()
