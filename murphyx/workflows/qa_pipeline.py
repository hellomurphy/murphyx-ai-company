"""
QA pipeline workflow — test a set of artifact refs; re-enqueue fix tasks on failure.

Escalates to PM if max retries exceeded.
"""

from __future__ import annotations

from murphyx.queue import redis_queue
from murphyx.queue.task_schema import FailurePolicy, TaskEnvelope

WORKFLOW_VERSION = "1"
QUEUE_NAME = "murphyx:tasks"


def create_qa_tasks(
    artifact_refs: list[str],
    *,
    parent_workflow_id: str = "",
) -> list[TaskEnvelope]:
    """Generate QA tasks for each artifact ref."""
    tasks: list[TaskEnvelope] = []
    for ref in artifact_refs:
        tasks.append(
            TaskEnvelope(
                type="test_qa",
                role_id="somjai_qa",
                payload={
                    "description": f"Run QA checks on artifact: {ref}",
                    "artifact_ref": ref,
                },
                workflow_id=parent_workflow_id,
                workflow_version=WORKFLOW_VERSION,
                failure_policy=FailurePolicy.RETRY,
                max_retries=2,
            )
        )
    return tasks


async def enqueue_qa_pipeline(
    artifact_refs: list[str],
    *,
    parent_workflow_id: str = "",
) -> list[str]:
    """Create QA tasks and push them onto the queue. Returns task ids."""
    tasks = create_qa_tasks(artifact_refs, parent_workflow_id=parent_workflow_id)
    ids: list[str] = []
    for t in tasks:
        await redis_queue.enqueue(QUEUE_NAME, t)
        ids.append(t.id)
    return ids
