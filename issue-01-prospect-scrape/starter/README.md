# Starter server

A runnable skeleton for the pattern in this teardown. It gives your coding agent a structure to build on instead of a blank file — same layout every time, whatever the data source is.

## Run it

```bash
cd starter
uv sync
uv run uvicorn main:app --reload
```

Open http://localhost:8000/docs for the interactive routes.

## The shape

| Route | Stage | What your agent builds on it |
|---|---|---|
| `POST /ingest` | ingest | accepts one record or a batch — one real record first |
| `GET /prospects` | rank | the ranked call list (recency x signal), `?status=` to filter |
| `GET /prospects/{company}` | serve | single prospect detail |
| `POST /run` | fetch | **the placeholder** — agent replaces this with your data source |
| `GET /healthz` | ops | liveness check for hosting |

The store is a Python list on purpose. Your agent's first job is wiring `/run` to a real source and ingesting real records; swap the store for sqlite/postgres when that works.

## Hand this to your coding agent

> This FastAPI app in `starter/` is a scaffold for a prospect-finder. Replace the `/run` placeholder with a fetcher for [YOUR DATA SOURCE], using the record shape in `main.py`. Here is one real record from the source: [PASTE IT]. Ingest a small sample through `/ingest`, verify each row matches the source, then rank by recency and signal. Do not invent field names — the record I pasted is the schema.

The one-real-record rule from the teardown applies here too: without a real record, the agent invents field names and builds against a schema that doesn't exist.
