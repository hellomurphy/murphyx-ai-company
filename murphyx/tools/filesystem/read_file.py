"""
Tool: read_file — read a file within a sandboxed allowlist.

Read-only; must not mutate state. Pydantic input/output schemas.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from murphyx.tools.base import ToolResult, run_with_timeout

ALLOWED_ROOTS: list[Path] = [
    Path.cwd(),
]


class ReadFileInput(BaseModel):
    path: str
    max_bytes: int = 100_000


class ReadFileOutput(BaseModel):
    content: str
    size: int


async def _read(inp: ReadFileInput) -> ReadFileOutput:
    target = Path(inp.path).resolve()
    if not any(target.is_relative_to(root) for root in ALLOWED_ROOTS):
        raise PermissionError(f"path outside sandbox: {target}")
    raw = target.read_text(encoding="utf-8")[:inp.max_bytes]
    return ReadFileOutput(content=raw, size=len(raw))


async def execute(inp: ReadFileInput, timeout: float = 10.0) -> ToolResult:
    return await run_with_timeout(_read(inp), timeout=timeout, tool_name="read_file")
