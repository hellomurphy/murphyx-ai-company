#!/usr/bin/env python3
"""
Quick start — execute a single task with a specific role.

Usage:
    python examples/run_single_agent.py

Demonstrates role binding, LLM completion, and artifact writing
without needing the full queue infrastructure.
"""

import asyncio

from murphyx.queue.task_schema import TaskEnvelope
from murphyx.runtime.agent_runtime import AgentRuntime


async def main() -> None:
    task = TaskEnvelope(
        type="implement_be",
        role_id="somsak_be",
        payload={
            "description": "Create a FastAPI health endpoint returning {status: ok}",
        },
    )
    runtime = AgentRuntime()
    try:
        output = await runtime.run_task(task)
        print("Agent output:")
        print(output)
    finally:
        await runtime.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
