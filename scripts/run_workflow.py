#!/usr/bin/env python3
"""Dev entry — run a named workflow and enqueue its tasks."""

import argparse
import asyncio

from murphyx.queue import redis_queue
from murphyx.workflows.build_saas import create_build_saas_tasks
from murphyx.workflows.qa_pipeline import enqueue_qa_pipeline
from murphyx.workflows.deploy_pipeline import enqueue_deploy_pipeline

QUEUE_NAME = "murphyx:tasks"


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run a MurphyX workflow")
    parser.add_argument("workflow", choices=["build_saas", "qa", "deploy"])
    parser.add_argument("--goal", default="Pet grooming SaaS MVP")
    parser.add_argument("--refs", nargs="*", default=[])
    args = parser.parse_args()

    if args.workflow == "build_saas":
        tasks = create_build_saas_tasks(args.goal)
        for t in tasks:
            await redis_queue.enqueue(QUEUE_NAME, t)
        print(f"Enqueued {len(tasks)} build_saas tasks")
    elif args.workflow == "qa":
        ids = await enqueue_qa_pipeline(args.refs)
        print(f"Enqueued {len(ids)} QA tasks")
    elif args.workflow == "deploy":
        ids = await enqueue_deploy_pipeline(args.refs)
        print(f"Enqueued {len(ids)} deploy tasks")

    await redis_queue.close()


if __name__ == "__main__":
    asyncio.run(main())
