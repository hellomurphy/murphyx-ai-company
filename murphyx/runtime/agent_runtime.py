"""
Agent runtime facade — wires Settings, queue, and LLM client.

Entry point for running the full MurphyX worker process.
"""

from __future__ import annotations

from murphyx.config import Settings, get_settings
from murphyx.observability import get_logger, log_event
from murphyx.queue import redis_queue
from murphyx.queue.task_schema import TaskEnvelope
from murphyx.runtime.worker_loop import QUEUE_NAME, _execute_task, run_worker_loop
from murphyx.services import llm_client

logger = get_logger("runtime")


class AgentRuntime:
    """Top-level handle: start workers, run single tasks, shutdown."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    async def start(self) -> None:
        """Spawn the worker loop (blocks until max_steps or cancellation)."""
        log_event(logger, "runtime_start", env=self.settings.environment)
        try:
            await run_worker_loop()
        finally:
            await self.shutdown()

    async def run_task(self, task: TaskEnvelope) -> str:
        """Single-shot task execution — useful for tests / API calls."""
        log_event(logger, "run_task", task_id=task.id)
        return await _execute_task(task)

    async def enqueue(self, task: TaskEnvelope) -> str:
        """Push a task onto the default queue."""
        return await redis_queue.enqueue(QUEUE_NAME, task)

    async def shutdown(self) -> None:
        await redis_queue.close()
        await llm_client.close()
        log_event(logger, "runtime_shutdown")
