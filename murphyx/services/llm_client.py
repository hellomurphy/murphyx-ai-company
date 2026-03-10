"""
LLM client — Ollama/vLLM compatible HTTP wrapper.

Scaffold; reads LLM_BASE_URL / LLM_MODEL from env. No API keys in code.
"""

# TODO: Implement chat completion with role-bound system prompt.


def complete(system: str, user: str) -> str:
    """Single completion — stub."""
    raise NotImplementedError
