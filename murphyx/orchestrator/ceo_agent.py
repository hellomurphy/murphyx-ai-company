"""
CEO agent ("Jarvis") — decompose a founder goal into a task graph.

Uses LLM with ceo_prompt.txt to output structured JSON. Validates with
Pydantic before enqueuing. No business/trading logic in this module.
"""

from __future__ import annotations

from pydantic import TypeAdapter

from murphyx.observability import get_logger, log_event
from murphyx.orchestrator.planner import build_plan
from murphyx.orchestrator.task_router import route_task
from murphyx.queue import redis_queue
from murphyx.queue.task_schema import TaskEnvelope
from murphyx.runtime.role_switcher import _load_prompt
from murphyx.services import llm_client

logger = get_logger("ceo")

_TASK_LIST_ADAPTER = TypeAdapter(list[TaskEnvelope])

QUEUE_NAME = "murphyx:tasks"

_DECOMPOSE_SUFFIX = """
Respond ONLY with a JSON array of task objects. Each object MUST have:
  - "type": one of plan, design_ux, implement_fe, implement_be,
    test_qa, deploy, write_docs, marketing_copy, sales_copy
  - "payload": dict with a "description" key (string)
  - "payload.depends_on": optional list of task ids this depends on
Do not add commentary outside the JSON array.
"""


async def plan_from_goal(goal: str) -> list[TaskEnvelope]:
    """
    Ask LLM to decompose *goal* into tasks, validate with Pydantic,
    run planner for ordering, assign role_ids via router, then enqueue.
    """
    system = _load_prompt("ceo") + "\n\n" + _DECOMPOSE_SUFFIX
    raw = await llm_client.complete(system=system, user=goal, max_tokens=4096)

    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("LLM did not return a JSON array")
    raw_json = raw[start : end + 1]

    tasks = _TASK_LIST_ADAPTER.validate_json(raw_json)
    log_event(logger, "decomposed", goal=goal[:80], task_count=len(tasks))

    ordered = build_plan(tasks)

    for task in ordered:
        role_id = route_task(task)
        task.role_id = role_id
        await redis_queue.enqueue(QUEUE_NAME, task)

    log_event(logger, "enqueued_all", task_count=len(ordered))
    return ordered
