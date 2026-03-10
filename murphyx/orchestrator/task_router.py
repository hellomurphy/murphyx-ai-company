"""
Task router — map task type to agent module / role id.

Scaffold only; no marketplace or pricing routes.
"""

from typing import Any


def route_task(task: dict[str, Any]) -> str:
    """Return role_id for worker binding — stub."""
    # TODO: task["type"] -> somchai_pm | somsak_backend | ...
    return task.get("role_id", "unknown")
