"""
LLM client — async httpx wrapper for Ollama and OpenAI-compatible APIs.

Reads provider / base_url / model / api_key from Settings.
Bounded prompts: caller must supply max_tokens for resource governance.
"""

from __future__ import annotations

import httpx

from murphyx.config import get_settings
from murphyx.observability import get_logger, log_event

logger = get_logger("llm")

_HTTP: httpx.AsyncClient | None = None


async def _get_http() -> httpx.AsyncClient:
    global _HTTP
    if _HTTP is None:
        _HTTP = httpx.AsyncClient(timeout=120.0)
    return _HTTP


async def complete(
    system: str,
    user: str,
    *,
    max_tokens: int = 2048,
    temperature: float = 0.2,
) -> str:
    """
    Single chat completion. Returns assistant text.
    Switches between Ollama (/api/chat) and OpenAI-compatible (/v1/chat/completions)
    based on Settings.llm_provider.
    """
    settings = get_settings()
    http = await _get_http()

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    if settings.llm_provider == "ollama":
        resp = await http.post(
            f"{settings.llm_base_url}/api/chat",
            json={
                "model": settings.llm_model,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                },
            },
        )
        resp.raise_for_status()
        text = resp.json()["message"]["content"]
    else:
        headers: dict[str, str] = {}
        if settings.llm_api_key:
            headers["Authorization"] = f"Bearer {settings.llm_api_key}"
        resp = await http.post(
            f"{settings.llm_base_url}/v1/chat/completions",
            headers=headers,
            json={
                "model": settings.llm_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"]

    log_event(
        logger, "completion",
        provider=settings.llm_provider,
        model=settings.llm_model,
        prompt_chars=len(system) + len(user),
        output_chars=len(text),
    )
    return text


async def close() -> None:
    global _HTTP
    if _HTTP is not None:
        await _HTTP.aclose()
        _HTTP = None
