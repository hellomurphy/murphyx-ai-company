"""
Tool: write_file — explicit write within sandboxed paths.

Idempotent when content is unchanged (skip rewrite if hash matches).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from pydantic import BaseModel

from murphyx.tools.base import ToolResult, run_with_timeout

ALLOWED_ROOTS: list[Path] = [
    Path.cwd(),
]


class WriteFileInput(BaseModel):
    path: str
    content: str


class WriteFileOutput(BaseModel):
    written: bool
    path: str
    size: int


async def _write(inp: WriteFileInput) -> WriteFileOutput:
    target = Path(inp.path).resolve()
    if not any(target.is_relative_to(root) for root in ALLOWED_ROOTS):
        raise PermissionError(f"path outside sandbox: {target}")
    new_hash = hashlib.sha256(inp.content.encode()).hexdigest()
    if target.exists():
        existing_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if existing_hash == new_hash:
            return WriteFileOutput(
                written=False, path=str(target), size=len(inp.content),
            )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(inp.content, encoding="utf-8")
    return WriteFileOutput(written=True, path=str(target), size=len(inp.content))


async def execute(inp: WriteFileInput, timeout: float = 10.0) -> ToolResult:
    return await run_with_timeout(_write(inp), timeout=timeout, tool_name="write_file")
