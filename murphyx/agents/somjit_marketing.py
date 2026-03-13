"""
Somjit — Growth marketing agent module.

Produces copy drafts and A/B variants. No ad account tokens.
"""

from __future__ import annotations

from typing import Any

from murphyx.runtime.role_switcher import bind_role, unbind_role
from murphyx.services import llm_client

ROLE_ID = "somjit_marketing"


async def handle_task(payload: dict[str, Any]) -> str:
    """Generate marketing copy from a task description."""
    ctx = bind_role(ROLE_ID)
    try:
        return await llm_client.complete(
            system=ctx.system_prompt,
            user=str(payload),
            max_tokens=ctx.token_budget,
        )
    finally:
        unbind_role()
