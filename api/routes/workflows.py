"""
Workflows routes — run named workflows (scaffold).

TODO: POST /workflows/run — e.g. build_saas, qa_pipeline.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.post("/run")
def run_workflow():
    """Stub."""
    return {"status": "not_implemented", "note": "scaffold — implementation TBD"}
