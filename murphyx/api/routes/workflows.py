"""Workflows routes — trigger named workflows."""

from pydantic import BaseModel
from fastapi import APIRouter

from murphyx.orchestrator.ceo_agent import plan_from_goal
from murphyx.queue import redis_queue
from murphyx.workflows.build_saas import create_build_saas_tasks

router = APIRouter(prefix="/workflows", tags=["workflows"])

QUEUE_NAME = "murphyx:tasks"


class GoalRequest(BaseModel):
    goal: str


class WorkflowRequest(BaseModel):
    name: str
    goal: str = ""
    artifact_refs: list[str] = []


@router.post("/run")
async def run_workflow(req: WorkflowRequest):
    """Trigger a named workflow and enqueue its tasks."""
    if req.name == "build_saas":
        tasks = create_build_saas_tasks(req.goal)
        ids = []
        for t in tasks:
            await redis_queue.enqueue(QUEUE_NAME, t)
            ids.append(t.id)
        return {"workflow": req.name, "task_ids": ids, "count": len(ids)}
    return {"error": f"unknown workflow: {req.name}"}


@router.post("/goal")
async def decompose_goal(req: GoalRequest):
    """Use the CEO agent to decompose a goal into tasks."""
    tasks = await plan_from_goal(req.goal)
    return {
        "task_count": len(tasks),
        "task_ids": [t.id for t in tasks],
    }
