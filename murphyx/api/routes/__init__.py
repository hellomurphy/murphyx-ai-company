"""API routes — aggregate routers."""

from murphyx.api.routes import agents, tasks, workflows

ROUTERS = [
    agents.router,
    tasks.router,
    workflows.router,
]

__all__ = ["ROUTERS", "agents", "tasks", "workflows"]
