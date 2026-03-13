"""
Somchai — Project Manager agent module.

Delegates to the runtime via role binding; no Jira secrets.
"""

from __future__ import annotations

from typing import Any

from murphyx.runtime.role_switcher import bind_role, unbind_role
from murphyx.services import llm_client

ROLE_ID = "somchai_pm"


async def handle_task(payload: dict[str, Any]) -> str:
    """Break a goal into scoped user stories with acceptance criteria."""
    ctx = bind_role(ROLE_ID)
    try:
        return await llm_client.complete(
            system=ctx.system_prompt,
            user=str(payload),
            max_tokens=ctx.token_budget,
        )
    finally:
        unbind_role()
