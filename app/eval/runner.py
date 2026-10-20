import json
from pathlib import Path

from app.eval.metrics import recall_at_k
from app.rag.retrieve import retrieve_top_chunks
from app.schemas import EvalQueryResult, EvalResponse

EVAL_PATH = Path(__file__).resolve().parents[2] / "data" / "eval" / "questions.json"


def load_eval_questions() -> list[dict]:
    return json.loads(EVAL_PATH.read_text())


def run_eval(k: int = 5) -> EvalResponse:
    queries: list[EvalQueryResult] = []
    for item in load_eval_questions():
        relevant = set(item["relevant_filenames"])
        results = retrieve_top_chunks(item["question"], limit=k)
        retrieved: list[str] = []
        for chunk in results:
            filename = str(chunk.extra_metadata.get("filename") or chunk.source_name)
            if filename not in retrieved:
                retrieved.append(filename)
        hits = sorted(relevant & set(retrieved[:k]))
        misses = sorted(relevant - set(retrieved[:k]))
        queries.append(
            EvalQueryResult(
                id=item["id"],
                question=item["question"],
                k=k,
                recall_at_k=recall_at_k(relevant, retrieved, k),
                relevant=sorted(relevant),
                retrieved=retrieved[:k],
                hits=hits,
                misses=misses,
                chunks=results,
            )
        )
    mean = sum(query.recall_at_k for query in queries) / len(queries) if queries else 0.0
    return EvalResponse(k=k, mean_recall_at_k=mean, queries=queries)
