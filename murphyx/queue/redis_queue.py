"""
Redis queue backend — async enqueue / dequeue / ack / nack.

Uses redis.asyncio; serializes TaskEnvelope via Pydantic JSON.
"""

from __future__ import annotations

import redis.asyncio as aioredis

from murphyx.config import get_settings
from murphyx.observability import get_logger, log_event
from murphyx.queue.task_schema import TaskEnvelope, TaskStatus

logger = get_logger("queue")

_POOL: aioredis.Redis | None = None


async def _get_client() -> aioredis.Redis:
    global _POOL
    if _POOL is None:
        _POOL = aioredis.from_url(
            get_settings().redis_url, decode_responses=True
        )
    return _POOL


async def enqueue(queue_name: str, task: TaskEnvelope) -> str:
    """Push task to the right of the list. Returns task id."""
    client = await _get_client()
    await client.rpush(queue_name, task.model_dump_json())
    log_event(logger, "enqueued", task_id=task.id, queue=queue_name, type=task.type)
    return task.id


async def dequeue(queue_name: str, timeout_sec: int = 5) -> TaskEnvelope | None:
    """Blocking left-pop. Returns None on timeout."""
    client = await _get_client()
    result = await client.blpop(queue_name, timeout=timeout_sec)
    if result is None:
        return None
    _, raw = result
    task = TaskEnvelope.model_validate_json(raw)
    task.status = TaskStatus.RUNNING
    log_event(logger, "dequeued", task_id=task.id, queue=queue_name)
    return task


async def ack(task: TaskEnvelope) -> None:
    """Mark task done — store result reference in a hash."""
    client = await _get_client()
    task.status = TaskStatus.DONE
    await client.hset("murphyx:completed", task.id, task.model_dump_json())
    log_event(logger, "ack", task_id=task.id)


async def nack(task: TaskEnvelope, queue_name: str) -> None:
    """Handle failure per failure policy: retry / escalate / abort."""
    task.retry_count += 1
    if task.should_retry():
        task.status = TaskStatus.PENDING
        await enqueue(queue_name, task)
        log_event(
            logger, "nack_retry",
            task_id=task.id, retry=task.retry_count, max=task.max_retries,
        )
    else:
        task.status = TaskStatus.DEAD_LETTER
        client = await _get_client()
        await client.rpush(f"{queue_name}:dead_letter", task.model_dump_json())
        log_event(
            logger, "nack_dead_letter",
            task_id=task.id, policy=task.failure_policy,
        )


async def close() -> None:
    global _POOL
    if _POOL is not None:
        await _POOL.aclose()
        _POOL = None
