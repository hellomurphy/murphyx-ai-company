"""
Role switcher — load system prompt + tool allowlist per task role.

One LLM, many costumes. Each task gets a clean context (no carry-over).
Prompts live in murphyx/prompts/ as plain text files per .cursorrules.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from murphyx.observability import get_logger, log_event
from murphyx.tools.registry import list_tools

logger = get_logger("role_switcher")

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

ROLE_TOOLS: dict[str, list[str]] = {
    "somchai_pm": [],
    "somruedee_ux": [],
    "saifah_fe": ["read_file", "write_file"],
    "somsak_be": ["read_file", "write_file"],
    "somjai_qa": ["read_file"],
    "sombat_devops": [],
    "somphop_docs": ["read_file"],
    "somjit_marketing": [],
    "somchok_sales": [],
    "somporn_cs": [],
}

DEFAULT_TOKEN_BUDGET = 2048


class RoleContext(BaseModel):
    """Returned by bind_role; consumed by worker loop / LLM client."""
    role_id: str
    system_prompt: str
    tools: list[str]
    token_budget: int = DEFAULT_TOKEN_BUDGET


def _load_prompt(role_id: str) -> str:
    candidates = [
        _PROMPTS_DIR / f"{role_id}_prompt.txt",
        _PROMPTS_DIR / f"{role_id.split('_')[0]}_prompt.txt",
    ]
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    return f"You are {role_id}. Complete the assigned task."


def bind_role(role_id: str) -> RoleContext:
    """Load prompt + tool allowlist for a role. Stateless — no carry-over."""
    prompt = _load_prompt(role_id)
    tools = ROLE_TOOLS.get(role_id, [])
    available = set(list_tools())
    resolved = [t for t in tools if t in available]

    ctx = RoleContext(
        role_id=role_id,
        system_prompt=prompt,
        tools=resolved,
    )
    log_event(logger, "bind", role_id=role_id, tools=resolved)
    return ctx


def unbind_role() -> None:
    """Explicit context boundary marker (no in-process state to clear currently)."""
    log_event(logger, "unbind")
