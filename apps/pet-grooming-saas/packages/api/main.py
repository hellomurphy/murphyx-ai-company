"""
FastAPI stub — health + placeholder routes.

TODO: Add appointments resource when backend workflow is wired.
No DB URL in code; use env (see root .env.example).
"""

from fastapi import FastAPI

app = FastAPI(title="Pet Grooming API", version="0.0.0-scaffold")


@app.get("/health")
def health():
    return {"status": "ok", "note": "scaffold — implementation TBD"}


# TODO: POST/GET /api/v1/appointments when ready
