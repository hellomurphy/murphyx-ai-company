"""
Agent runtime facade — single entry for dequeue → bind → execute → handoff.

Comparable in scope to a thin CrewAI/LangGraph runner; MurphyX-specific
orchestration lives in murphyx/orchestrator/. Scaffold only.
"""

from typing import Any


class AgentRuntime:
    """Coordinates worker loop + role switcher + queue — stub."""

    def __init__(self) -> None:
        # TODO: Inject queue backend + LLM client.
        pass

    def run_task(self, task_id: str) -> dict[str, Any]:
        """Execute one task — NotImplemented until pipeline exists."""
        raise NotImplementedError("AgentRuntime.run_task — to be implemented")
