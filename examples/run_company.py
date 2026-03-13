#!/usr/bin/env python3
"""
Quick start — submit a founder goal, let CEO decompose it, then run the worker.

Usage:
    python examples/run_company.py "Build a pet grooming SaaS MVP"

Requires Redis running (see scripts/start_redis.sh) and an LLM provider
configured in .env (defaults to Ollama on localhost:11434).
"""

import asyncio
import sys

from murphyx.orchestrator.ceo_agent import plan_from_goal
from murphyx.runtime.agent_runtime import AgentRuntime


async def main(goal: str) -> None:
    tasks = await plan_from_goal(goal)
    print(f"CEO decomposed goal into {len(tasks)} tasks:")
    for t in tasks:
        print(f"  [{t.type}] {t.id} -> {t.role_id}")

    runtime = AgentRuntime()
    print("\nStarting worker loop (Ctrl+C to stop)...")
    await runtime.start()


if __name__ == "__main__":
    goal = " ".join(sys.argv[1:]) or "Build a pet grooming SaaS MVP"
    asyncio.run(main(goal))
