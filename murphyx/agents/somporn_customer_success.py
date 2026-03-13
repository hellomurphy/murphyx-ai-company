"""
Somporn — Customer success agent module.

Generates support responses and onboarding content. No customer PII.
"""

from __future__ import annotations

from typing import Any

from murphyx.runtime.role_switcher import bind_role, unbind_role
from murphyx.services import llm_client

ROLE_ID = "somporn_cs"


async def handle_task(payload: dict[str, Any]) -> str:
    """Draft customer support or onboarding content."""
    ctx = bind_role(ROLE_ID)
    try:
        return await llm_client.complete(
            system=ctx.system_prompt,
            user=str(payload),
            max_tokens=ctx.token_budget,
        )
    finally:
        unbind_role()
