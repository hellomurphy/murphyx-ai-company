#!/usr/bin/env python3
"""
Quick start — trigger the build_saas workflow and enqueue all tasks.

Usage:
    python examples/run_saas_builder.py

Requires Redis running. Worker loop must be running separately
(scripts/run_worker.sh) to process the enqueued tasks.
"""

import asyncio

from murphyx.queue import redis_queue
from murphyx.workflows.build_saas import create_build_saas_tasks

QUEUE_NAME = "murphyx:tasks"


async def main() -> None:
    tasks = create_build_saas_tasks("Pet grooming SaaS for modern salons")
    print(f"Build SaaS workflow: {len(tasks)} tasks")
    for t in tasks:
        await redis_queue.enqueue(QUEUE_NAME, t)
        print(f"  enqueued [{t.type}] {t.id} -> {t.role_id}")
    print("\nDone. Run scripts/run_worker.sh to process tasks.")
    await redis_queue.close()


if __name__ == "__main__":
    asyncio.run(main())
