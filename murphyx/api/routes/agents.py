"""Agents routes — list registered roles and their tool allowlists."""

from fastapi import APIRouter

from murphyx.orchestrator.task_router import TASK_TYPE_TO_ROLE
from murphyx.runtime.role_switcher import ROLE_TOOLS

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def list_agents():
    """Return all registered agent roles with their tool access."""
    agents = []
    for role_id, tools in ROLE_TOOLS.items():
        task_types = [k for k, v in TASK_TYPE_TO_ROLE.items() if v == role_id]
        agents.append({
            "role_id": role_id,
            "tools": tools,
            "handles_task_types": task_types,
        })
    return {"agents": agents, "count": len(agents)}
