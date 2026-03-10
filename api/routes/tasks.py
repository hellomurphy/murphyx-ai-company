"""
Tasks routes — enqueue/dequeue control (scaffold).

TODO: POST /tasks, GET /tasks/{id} — queue abstraction only.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("")
def create_task():
    """Stub."""
    return {"id": None, "note": "scaffold — implementation TBD"}
