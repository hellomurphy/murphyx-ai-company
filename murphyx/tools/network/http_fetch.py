"""
Tool: http_fetch — GET a URL within an allowlist; timeout + circuit breaker.
"""

from __future__ import annotations

import httpx
from pydantic import BaseModel

from murphyx.tools.base import ToolResult, run_with_timeout
from murphyx.tools.circuit_breaker import CircuitBreaker

URL_ALLOWLIST: list[str] = []

_breaker = CircuitBreaker("http_fetch", threshold=10, cooldown_sec=60.0)


class HttpFetchInput(BaseModel):
    url: str
    max_bytes: int = 500_000


class HttpFetchOutput(BaseModel):
    status_code: int
    body: str
    size: int


async def _fetch(inp: HttpFetchInput) -> HttpFetchOutput:
    allowed = any(inp.url.startswith(p) for p in URL_ALLOWLIST)
    if URL_ALLOWLIST and not allowed:
        raise PermissionError(f"url outside allowlist: {inp.url}")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(inp.url)
        body = resp.text[:inp.max_bytes]
    _breaker.record_success()
    return HttpFetchOutput(status_code=resp.status_code, body=body, size=len(body))


async def execute(inp: HttpFetchInput, timeout: float = 30.0) -> ToolResult:
    if _breaker.is_open:
        return ToolResult(success=False, error="circuit breaker open for http_fetch")
    result = await run_with_timeout(
        _fetch(inp), timeout=timeout, tool_name="http_fetch",
    )
    if not result.success:
        _breaker.record_failure()
    return result
