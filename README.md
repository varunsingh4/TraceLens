# TraceLens

Evidence-backed AI investigator for production incidents.

TraceLens retrieves stack traces, runbooks, release notes, and past issues for an incident question, then scores that retrieval with **Recall@k**.

## What it does

| Surface | Purpose |
|---|---|
| Investigate UI | Ask a question and inspect the top-k chunks plus source metadata |
| Recall@k UI | Run a labeled eval set and see hits, misses, and mean Recall@k |
| `POST /ingest` | Store a document with `source_type` / `source_name` |
| `GET /retrieve` | Return the top-k similar chunks |
| `GET /eval` | Score labeled questions from `data/eval/questions.json` |

```text
question  →  embed  →  Qdrant nearest neighbors  →  evidence chunks
                              ▲
document  →  chunk  →  embed ─┘
                │
                └── Postgres (full text + metadata)
```

**Recall@k** is the share of labeled-relevant documents that appear in the top *k* retrieved results:

`Recall@k = |relevant ∩ retrieved[:k]| / |relevant|`

Gold labels live in `data/eval/questions.json`. Change those filenames to evaluate your own corpus.

## Stack

Python, FastAPI, Qdrant, PostgreSQL, Docker Compose, local MiniLM embeddings (`sentence-transformers/all-MiniLM-L6-v2`).

## Quick start

```bash
docker compose up -d
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.seed
uvicorn app.main:app --reload --reload-dir app --port 8000
```

Open:

- UI: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

Postgres is mapped to **5433** so it is less likely to clash with a local Postgres on 5432.

The first process start downloads the embedding model and can take a minute.

## Project layout

```text
app/
  main.py              UI + ingest + retrieve + eval routes
  eval/metrics.py      Recall@k
  eval/runner.py       labeled eval over the live index
  rag/                 chunking, embeddings, ingest, Qdrant
  static/              Investigate and Recall@k UI
data/samples/          demo stack traces, docs, release notes, past issues
data/eval/             gold questions for Recall@k
```

## Verify

```bash
pytest -q
curl -sG http://127.0.0.1:8000/retrieve \
  --data-urlencode 'question=Why did checkout return 500 after the 1.4.2 deploy?'
curl -s 'http://127.0.0.1:8000/eval?k=5'
```
