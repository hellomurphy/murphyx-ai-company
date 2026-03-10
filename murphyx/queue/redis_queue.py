"""
Redis queue backend — enqueue/dequeue/ack.

Scaffold; connect via REDIS_URL from env. No task payloads with secrets.
"""

# TODO: Implement with redis-py; use task_schema for serialization.


def enqueue(queue_name: str, task: dict) -> str:
    """Push task — stub."""
    raise NotImplementedError


def dequeue(queue_name: str, timeout_sec: int = 5) -> dict | None:
    """Blocking pop — stub."""
    raise NotImplementedError
