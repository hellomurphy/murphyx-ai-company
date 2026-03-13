"""
Worker loop — async consumer: dequeue -> bind role -> LLM -> artifact -> unbind.

Pillar 1: while-True for blocking dequeue is allowed; branching via router.
Failure policy: retry / escalate / abort per task.
"""

from __future__ import annotations

import asyncio
import json

from murphyx.config import get_settings
from murphyx.observability import get_logger, log_event
from murphyx.queue import TaskEnvelope
from murphyx.queue import redis_queue
from murphyx.runtime.role_switcher import bind_role, unbind_role
from murphyx.services import llm_client
from murphyx.services.artifact_store import task_artifact_dir

logger = get_logger("worker")

QUEUE_NAME = "murphyx:tasks"
MAX_STEPS = 1000


async def _execute_task(task: TaskEnvelope) -> str:
    """Bind role, call LLM, write artifact, unbind. Returns output text."""
    ctx = bind_role(task.role_id)
    try:
        user_prompt = json.dumps(task.payload, default=str)
        output = await llm_client.complete(
            system=ctx.system_prompt,
            user=user_prompt,
            max_tokens=ctx.token_budget,
        )
        out_dir = task_artifact_dir(task.id)
        (out_dir / "output.txt").write_text(output, encoding="utf-8")
        task.artifact_refs.append(f"{task.id}/output.txt")
        return output
    finally:
        unbind_role()


async def run_worker_loop() -> None:
    """Main consumer loop — runs until cancelled or max_steps reached."""
    settings = get_settings()
    log_event(logger, "worker_start", env=settings.environment)
    steps = 0

    while steps < MAX_STEPS:
        task = await redis_queue.dequeue(QUEUE_NAME, timeout_sec=5)
        if task is None:
            continue

        steps += 1
        log_event(
            logger, "task_start",
            task_id=task.id, type=task.type, role=task.role_id, step=steps,
        )

        try:
            await _execute_task(task)
            await redis_queue.ack(task)
            log_event(logger, "task_done", task_id=task.id)
        except Exception as exc:
            log_event(logger, "task_fail", task_id=task.id, error=str(exc))
            await redis_queue.nack(task, QUEUE_NAME)

    log_event(logger, "worker_stop", reason="max_steps", steps=steps)


if __name__ == "__main__":
    asyncio.run(run_worker_loop())
