"""
Tests for runtime — task schema validation, router mapping, planner ordering.
"""

from murphyx.orchestrator.task_router import route_task, TERMINAL
from murphyx.orchestrator.planner import build_plan
from murphyx.queue.task_schema import FailurePolicy, TaskEnvelope, TaskStatus


def test_task_envelope_defaults():
    t = TaskEnvelope(type="plan", payload={"goal": "test"})
    assert t.status == TaskStatus.PENDING
    assert t.failure_policy == FailurePolicy.RETRY
    assert t.max_retries == 3
    assert t.retry_count == 0
    assert len(t.id) == 12
    assert t.created_at


def test_should_retry():
    t = TaskEnvelope(type="plan", max_retries=2, retry_count=1)
    assert t.should_retry() is True
    t.retry_count = 2
    assert t.should_retry() is False


def test_router_known_type():
    t = TaskEnvelope(type="implement_be")
    role = route_task(t)
    assert role == "somsak_be"


def test_router_unknown_type():
    t = TaskEnvelope(type="unknown_type_xyz")
    role = route_task(t)
    assert role == TERMINAL


def test_planner_topological_order():
    a = TaskEnvelope(id="a", type="plan", payload={})
    b = TaskEnvelope(id="b", type="implement_fe", payload={"depends_on": ["a"]})
    c = TaskEnvelope(id="c", type="test_qa", payload={"depends_on": ["b"]})
    ordered = build_plan([c, a, b])
    ids = [t.id for t in ordered]
    assert ids.index("a") < ids.index("b")
    assert ids.index("b") < ids.index("c")
    assert all(t.workflow_id for t in ordered)


def test_planner_assigns_workflow_version():
    a = TaskEnvelope(id="x", type="plan", payload={})
    ordered = build_plan([a], workflow_version="2")
    assert ordered[0].workflow_version == "2"
