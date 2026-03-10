"""
Role switcher — load system prompt + tool allowlist per task role.

One LLM, many costumes. No parallel Som-* in the same forward pass.
Scaffold only; prompt paths and binding logic to be added later.
"""

from typing import Any


def bind_role(role_id: str, task_context: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Return runtime context for the given role (prompts, tools, memory slice).
    Stub returns empty dict until prompts/ and agents/ are wired.
    """
    # TODO: Resolve role_id -> prompt file + optional memory slice.
    return {"role_id": role_id, "task_context": task_context or {}}


def unbind_role() -> None:
    """Clear role-bound state between tasks — placeholder."""
    pass
