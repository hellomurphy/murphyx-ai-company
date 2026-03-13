"""
Task schema — strongly typed queue payloads (Pydantic V2).

Every task must have: id, type, payload, status, created_at.
Extend only here; do not scatter ad-hoc task dicts across call sites.
"""

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class FailurePolicy(StrEnum):
    RETRY = "retry"
    ESCALATE = "escalate"
    ABORT = "abort"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _uuid() -> str:
    return uuid4().hex[:12]


class TaskEnvelope(BaseModel):
    """Canonical task shape for queue + workers."""

    id: str = Field(default_factory=_uuid)
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = Field(default_factory=_now_iso)

    role_id: str = ""
    correlation_id: str = ""

    parent_task_id: str | None = None
    workflow_id: str = ""
    workflow_version: str = "1"

    artifact_refs: list[str] = Field(default_factory=list)

    failure_policy: FailurePolicy = FailurePolicy.RETRY
    max_retries: int = 3
    retry_count: int = 0

    def should_retry(self) -> bool:
        return (
            self.failure_policy == FailurePolicy.RETRY
            and self.retry_count < self.max_retries
        )
