"""
Tool registry — name -> module lookup for role switcher.
"""

from __future__ import annotations

from typing import Any

TOOL_REGISTRY: dict[str, Any] = {}


def register_defaults() -> None:
    """Populate registry with built-in tools."""
    from murphyx.tools.filesystem import read_file, write_file
    from murphyx.tools.compute import calculator
    from murphyx.tools.network import http_fetch

    TOOL_REGISTRY.update({
        "read_file": read_file,
        "write_file": write_file,
        "calculator": calculator,
        "http_fetch": http_fetch,
    })


def get_tool(name: str) -> Any:
    if not TOOL_REGISTRY:
        register_defaults()
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        raise KeyError(f"tool not registered: {name}")
    return tool


def list_tools() -> list[str]:
    if not TOOL_REGISTRY:
        register_defaults()
    return list(TOOL_REGISTRY.keys())
