"""
API routes package — aggregate routers for main app.

All routers are stubs; safe for public repo.
"""

from api.routes import agents, tasks, workflows

# Single list for main.py to loop — add new modules here when created.
ROUTERS = [
    agents.router,
    tasks.router,
    workflows.router,
]

__all__ = ["ROUTERS", "agents", "tasks", "workflows"]
