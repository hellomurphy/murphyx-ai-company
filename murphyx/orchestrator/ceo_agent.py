"""
CEO agent ("Jarvis") — cloud-side planning, decomposition, delegation.

Scaffold only. No trading/pricing logic; high-level task graph only.
"""

from typing import Any


def plan_from_goal(goal: str) -> list[dict[str, Any]]:
    """
    Turn founder goal into ordered task list — stub.
    """
    # TODO: LLM call with ceo_prompt.txt; output task graph for queue.
    raise NotImplementedError("ceo_agent.plan_from_goal — to be implemented")
