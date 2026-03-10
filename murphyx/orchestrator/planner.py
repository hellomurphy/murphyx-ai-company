"""
Planner — milestones, dependencies, and enqueue order.

Scaffold; safe for public repo. Replace with real planner when orchestrator is live.
"""

from typing import Any


def build_plan(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Topological sort / dependency resolution — stub."""
    # TODO: Respect task dependencies and priority.
    return tasks
