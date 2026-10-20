from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.eval.runner import run_eval
from app.rag.embeddings import get_model
from app.rag.ingest import ingest_document
from app.rag.retrieve import retrieve_top_chunks
from app.rag.vectorstore import ensure_collection
from app.schemas import EvalResponse, IngestRequest, IngestResponse, RetrieveResponse

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    get_model()
    ensure_collection()
    yield


app = FastAPI(
    title="TraceLens",
    description="Investigate incidents and measure retrieval Recall@k.",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def ui() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest(payload: IngestRequest, db: Session = Depends(get_db)) -> IngestResponse:
    document = ingest_document(db, payload)
    return IngestResponse(
        document_id=document.id,
        source_type=document.source_type,
        source_name=document.source_name,
        chunk_count=len(document.chunks),
    )


@app.get("/retrieve", response_model=RetrieveResponse)
def retrieve(
    question: str = Query(..., min_length=3, examples=["Why did checkout return 500 after deploy?"]),
    limit: int = Query(5, ge=1, le=10),
) -> RetrieveResponse:
    return RetrieveResponse(question=question, results=retrieve_top_chunks(question, limit=limit))


@app.get("/eval", response_model=EvalResponse)
def evaluate(k: int = Query(5, ge=1, le=10)) -> EvalResponse:
    return run_eval(k=k)
