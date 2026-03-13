"""
Tests for queue — enqueue/dequeue round-trip, ack, nack with fakeredis.
"""

import pytest
import fakeredis.aioredis

from murphyx.queue import redis_queue
from murphyx.queue.task_schema import FailurePolicy, TaskEnvelope, TaskStatus

QUEUE = "test:tasks"


@pytest.fixture(autouse=True)
async def _patch_redis(monkeypatch):
    """Replace the real Redis pool with fakeredis for every test."""
    fake = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(redis_queue, "_POOL", fake)
    yield
    await fake.aclose()


@pytest.mark.asyncio
async def test_enqueue_dequeue_roundtrip():
    task = TaskEnvelope(type="plan", payload={"goal": "test"})
    await redis_queue.enqueue(QUEUE, task)
    got = await redis_queue.dequeue(QUEUE, timeout_sec=1)
    assert got is not None
    assert got.id == task.id
    assert got.type == "plan"
    assert got.status == TaskStatus.RUNNING


@pytest.mark.asyncio
async def test_ack_stores_completed():
    task = TaskEnvelope(type="plan", payload={"goal": "ack-test"})
    await redis_queue.enqueue(QUEUE, task)
    got = await redis_queue.dequeue(QUEUE, timeout_sec=1)
    assert got is not None
    await redis_queue.ack(got)
    assert got.status == TaskStatus.DONE
    client = await redis_queue._get_client()
    raw = await client.hget("murphyx:completed", got.id)
    assert raw is not None


@pytest.mark.asyncio
async def test_nack_retries_then_dead_letter():
    task = TaskEnvelope(
        type="plan", payload={}, max_retries=2,
        failure_policy=FailurePolicy.RETRY,
    )
    await redis_queue.enqueue(QUEUE, task)
    got = await redis_queue.dequeue(QUEUE, timeout_sec=1)
    assert got is not None

    await redis_queue.nack(got, QUEUE)
    assert got.retry_count == 1
    retried = await redis_queue.dequeue(QUEUE, timeout_sec=1)
    assert retried is not None

    await redis_queue.nack(retried, QUEUE)
    assert retried.status == TaskStatus.DEAD_LETTER


@pytest.mark.asyncio
async def test_dequeue_returns_none_on_empty():
    got = await redis_queue.dequeue(QUEUE, timeout_sec=1)
    assert got is None
