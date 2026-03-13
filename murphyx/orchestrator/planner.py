"""
Planner — topological sort of tasks by depends_on field.

Assigns workflow_id + workflow_version. Deterministic given same input.
"""

from __future__ import annotations

from collections import defaultdict, deque
from uuid import uuid4

from murphyx.observability import get_logger, log_event
from murphyx.queue.task_schema import TaskEnvelope

logger = get_logger("planner")


def build_plan(
    tasks: list[TaskEnvelope],
    *,
    workflow_version: str = "1",
) -> list[TaskEnvelope]:
    """
    Topological sort by dependency adjacency.

    Each task may carry a `depends_on` list in its payload. Tasks without
    dependencies or whose dependencies are not in the batch are placed first.
    """
    workflow_id = uuid4().hex[:12]

    id_to_task = {t.id: t for t in tasks}
    in_degree: dict[str, int] = defaultdict(int)
    graph: dict[str, list[str]] = defaultdict(list)

    for t in tasks:
        deps: list[str] = t.payload.get("depends_on", [])
        for dep in deps:
            if dep in id_to_task:
                graph[dep].append(t.id)
                in_degree[t.id] += 1
        in_degree.setdefault(t.id, 0)

    queue: deque[str] = deque(
        tid for tid, deg in in_degree.items() if deg == 0
    )
    ordered: list[TaskEnvelope] = []

    while queue:
        tid = queue.popleft()
        task = id_to_task[tid]
        task.workflow_id = workflow_id
        task.workflow_version = workflow_version
        ordered.append(task)
        for child in graph[tid]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    if len(ordered) != len(tasks):
        log_event(logger, "cycle_detected", workflow_id=workflow_id)
        remaining = [t for t in tasks if t.id not in {o.id for o in ordered}]
        for t in remaining:
            t.workflow_id = workflow_id
            t.workflow_version = workflow_version
        ordered.extend(remaining)

    log_event(
        logger, "plan_built",
        workflow_id=workflow_id, version=workflow_version, task_count=len(ordered),
    )
    return ordered
