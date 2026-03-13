"""
Base tool protocol — every tool must expose typed input/output and a timeout.
"""

from __future__ import annotations

import asyncio
from typing import Any

from pydantic import BaseModel

from murphyx.observability import get_logger, log_event

logger = get_logger("tool")

DEFAULT_TIMEOUT_SEC = 30


class ToolResult(BaseModel):
    success: bool
    data: Any = None
    error: str | None = None


async def run_with_timeout(
    coro: Any,
    timeout: float = DEFAULT_TIMEOUT_SEC,
    tool_name: str = "unknown",
) -> ToolResult:
    """Wrap a tool coroutine with asyncio timeout + structured log."""
    try:
        result = await asyncio.wait_for(coro, timeout=timeout)
        log_event(logger, "tool_ok", tool=tool_name)
        return ToolResult(success=True, data=result)
    except asyncio.TimeoutError:
        log_event(logger, "tool_timeout", tool=tool_name, timeout=timeout)
        return ToolResult(success=False, error=f"timeout after {timeout}s")
    except Exception as exc:
        log_event(logger, "tool_error", tool=tool_name, error=str(exc))
        return ToolResult(success=False, error=str(exc))
