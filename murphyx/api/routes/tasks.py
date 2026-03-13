"""Tasks routes — enqueue tasks and query status."""

from fastapi import APIRouter

from murphyx.orchestrator.task_router import route_task
from murphyx.queue import redis_queue
from murphyx.queue.task_schema import TaskEnvelope

router = APIRouter(prefix="/tasks", tags=["tasks"])

QUEUE_NAME = "murphyx:tasks"


@router.post("")
async def create_task(task: TaskEnvelope):
    """Validate, assign role, and enqueue a task."""
    if not task.role_id:
        task.role_id = route_task(task)
    task_id = await redis_queue.enqueue(QUEUE_NAME, task)
    return {"id": task_id, "role_id": task.role_id, "status": task.status}


@router.get("/{task_id}")
async def get_task(task_id: str):
    """Look up a completed task by id (from Redis hash)."""
    client = await redis_queue._get_client()
    raw = await client.hget("murphyx:completed", task_id)
    if raw is None:
        return {"error": "not_found", "task_id": task_id}
    return TaskEnvelope.model_validate_json(raw).model_dump()
