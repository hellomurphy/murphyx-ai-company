"""
GitHub service — PR / issue helpers via httpx.

Uses GITHUB_TOKEN from env only — never commit token.
"""

from __future__ import annotations

import os

import httpx

from murphyx.observability import get_logger

logger = get_logger("github")

API_BASE = "https://api.github.com"


async def create_pr(
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = "main",
) -> dict:
    """Open a pull request on GitHub."""
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        return {"error": "GITHUB_TOKEN not set"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{API_BASE}/repos/{repo}/pulls",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            json={"title": title, "body": body, "head": head, "base": base},
        )
        resp.raise_for_status()
        data = resp.json()
    return {"pr_url": data.get("html_url"), "number": data.get("number")}
