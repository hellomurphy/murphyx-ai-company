"""
Agents routes — list/register agents (scaffold).

TODO: GET /agents, POST /agents/assign — framework only.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def list_agents():
    """Stub — return registered role ids when runtime exists."""
    return {"agents": [], "note": "scaffold — implementation TBD"}
