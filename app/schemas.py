from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    source_type: str = Field(
        examples=["stack_trace", "documentation", "release_notes", "past_issue"]
    )
    source_name: str = Field(examples=["checkout-service-prod-2026-10-20.log"])
    content: str
    extra_metadata: dict[str, Any] = Field(default_factory=dict)


class IngestResponse(BaseModel):
    document_id: UUID
    source_type: str
    source_name: str
    chunk_count: int


class RetrievedChunk(BaseModel):
    rank: int
    score: float
    chunk_id: UUID
    document_id: UUID
    source_type: str
    source_name: str
    chunk_index: int
    content: str
    extra_metadata: dict[str, Any] = Field(default_factory=dict)


class RetrieveResponse(BaseModel):
    question: str
    results: list[RetrievedChunk]


class EvalQueryResult(BaseModel):
    id: str
    question: str
    k: int
    recall_at_k: float
    relevant: list[str]
    retrieved: list[str]
    hits: list[str]
    misses: list[str]
    chunks: list[RetrievedChunk]


class EvalResponse(BaseModel):
    k: int
    mean_recall_at_k: float
    queries: list[EvalQueryResult]
