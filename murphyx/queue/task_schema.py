"""
Task schema — typed dict / dataclass for queue payloads.

Public-safe fields only: role_id, type, payload_ref, correlation_id.
"""

from typing import Any, TypedDict


class TaskEnvelope(TypedDict, total=False):
    """Minimal task shape — extend when runtime is implemented."""
    id: str
    role_id: str
    type: str
    payload: dict[str, Any]
    correlation_id: str
