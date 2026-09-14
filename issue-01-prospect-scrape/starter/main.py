"""Starter server for the prospect-scrape pattern (The Cactus Dispatch, Issue #1).

The pipeline shape is always the same, whatever the data source is:

    ingest -> detect (who is in the problem state) -> rank (recency x signal) -> serve

This file gives you that skeleton with the data-source part left open.
The in-memory store is deliberate: one real record first, structure second.
Swap it for sqlite/postgres the day the data outgrows a Python list.

Run it:
    uv sync
    uv run uvicorn main:app --reload
"""

import os

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="prospect-scrape starter", version="0.1.0")

# ponytail: in-memory store with a low ceiling — swap for sqlite/postgres once
# a real pipeline writes to it. Upgrade path: replace RECORD with a session.
RECORD: list[dict] = [
    {
        "company": "Example Import Co",
        "source_url": "https://example.com/record",
        "status": "exposed",          # free-form: your industry's problem state
        "state_changed_at": "2026-09-01",  # ISO date — recency drives the rank
        "signal": 42,                 # strength of buying signal (volume, spend, ...)
    }
]


class Record(BaseModel):
    company: str
    source_url: str
    status: str = Field(description="Your problem state, e.g. 'lapsed', 'expired', 'churned'")
    state_changed_at: str = Field(description="ISO date the company entered the problem state")
    signal: int = Field(default=0, description="Buying-signal strength; bigger = more urgent")


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True, "records": len(RECORD)}


@app.post("/ingest")
def ingest(records: Record | list[Record]) -> dict:
    """One real record first. A batch is fine; a hallucinated schema is not."""
    added = records if isinstance(records, list) else [records]
    RECORD.extend(r.model_dump() for r in added)
    return {"ingested": len(added), "total": len(RECORD)}


@app.get("/prospects")
def prospects(status: str | None = None) -> list[dict]:
    """Ranked call list: most recently in the problem state, strongest signal first."""
    rows = [r for r in RECORD if status is None or r["status"] == status]
    return sorted(rows, key=lambda r: (r["state_changed_at"], r["signal"]), reverse=True)


@app.get("/prospects/{company}")
def prospect(company: str) -> dict:
    for r in RECORD:
        if r["company"].lower() == company.lower():
            return r
    raise HTTPException(status_code=404, detail=f"no record for {company!r}")


@app.post("/run")
def run() -> dict:
    """Where your agent wires the real data source.

    Hand your coding agent this file plus the prompt from the README.
    Its job: replace this placeholder with code that pulls records from
    your source and POSTs them to /ingest (or writes to your database).
    """
    raise HTTPException(
        status_code=501,
        detail="Not built yet. This is the hook for your data source — see README.",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
