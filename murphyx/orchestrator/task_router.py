"""
Task router — map task.type to a role_id.

Thin layer: returns the next role_id or a terminal state. Must not
perform heavy computation (see .cursorrules, Pillar 1).
"""

from __future__ import annotations

from murphyx.observability import get_logger, log_event
from murphyx.queue.task_schema import TaskEnvelope

logger = get_logger("router")

TASK_TYPE_TO_ROLE: dict[str, str] = {
    "plan": "somchai_pm",
    "design_ux": "somruedee_ux",
    "implement_fe": "saifah_fe",
    "implement_be": "somsak_be",
    "test_qa": "somjai_qa",
    "deploy": "sombat_devops",
    "write_docs": "somphop_docs",
    "marketing_copy": "somjit_marketing",
    "sales_copy": "somchok_sales",
    "customer_success": "somporn_cs",
    "ceo_decompose": "ceo",
}

TERMINAL = "__done__"


def route_task(task: TaskEnvelope) -> str:
    """Return role_id for the task type, or TERMINAL if type is unknown."""
    role_id = TASK_TYPE_TO_ROLE.get(task.type)
    if role_id is None:
        log_event(logger, "route_miss", task_id=task.id, type=task.type)
        return TERMINAL
    log_event(logger, "route_hit", task_id=task.id, type=task.type, role=role_id)
    return role_id


def register_type(task_type: str, role_id: str) -> None:
    """Extend router at runtime (e.g. plugin roles)."""
    TASK_TYPE_TO_ROLE[task_type] = role_id
