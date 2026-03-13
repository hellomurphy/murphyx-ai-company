"""
Deploy pipeline workflow — Docker build + health check tasks.

No cloud provider secrets; environment config comes from Settings / env vars.
"""

from __future__ import annotations

from murphyx.queue import redis_queue
from murphyx.queue.task_schema import FailurePolicy, TaskEnvelope

WORKFLOW_VERSION = "1"
QUEUE_NAME = "murphyx:tasks"


def create_deploy_tasks(
    artifact_refs: list[str],
    *,
    parent_workflow_id: str = "",
) -> list[TaskEnvelope]:
    """Generate deployment tasks for the given artifacts."""
    build = TaskEnvelope(
        id="deploy-build",
        type="deploy",
        role_id="sombat_devops",
        payload={
            "description": "Build Docker images from artifact refs",
            "artifact_refs": artifact_refs,
        },
        workflow_id=parent_workflow_id,
        workflow_version=WORKFLOW_VERSION,
        failure_policy=FailurePolicy.ABORT,
    )
    health = TaskEnvelope(
        id="deploy-health",
        type="deploy",
        role_id="sombat_devops",
        payload={
            "description": "Run health checks against newly deployed containers",
            "depends_on": ["deploy-build"],
        },
        workflow_id=parent_workflow_id,
        workflow_version=WORKFLOW_VERSION,
        failure_policy=FailurePolicy.ESCALATE,
    )
    return [build, health]


async def enqueue_deploy_pipeline(
    artifact_refs: list[str],
    *,
    parent_workflow_id: str = "",
) -> list[str]:
    """Create deploy tasks and push them onto the queue."""
    tasks = create_deploy_tasks(artifact_refs, parent_workflow_id=parent_workflow_id)
    ids: list[str] = []
    for t in tasks:
        await redis_queue.enqueue(QUEUE_NAME, t)
        ids.append(t.id)
    return ids
