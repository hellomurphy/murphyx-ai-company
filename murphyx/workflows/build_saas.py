"""
Build SaaS workflow — PM -> UX -> FE -> BE -> QA -> DevOps -> Docs.

Produces an ordered list[TaskEnvelope] with dependencies, versioning,
and an execution budget. No proprietary product logic.
"""

from __future__ import annotations

from murphyx.orchestrator.planner import build_plan
from murphyx.queue.task_schema import FailurePolicy, TaskEnvelope

WORKFLOW_VERSION = "1"
MAX_STEPS = 7


def create_build_saas_tasks(goal: str) -> list[TaskEnvelope]:
    """Generate the canonical SaaS build pipeline for *goal*."""

    pm = TaskEnvelope(
        id="saas-pm",
        type="plan",
        role_id="somchai_pm",
        payload={"description": f"Break down SaaS goal into user stories: {goal}"},
    )
    ux = TaskEnvelope(
        id="saas-ux",
        type="design_ux",
        role_id="somruedee_ux",
        payload={
            "description": "Design wireframes and user flows for the SaaS product",
            "depends_on": ["saas-pm"],
        },
    )
    fe = TaskEnvelope(
        id="saas-fe",
        type="implement_fe",
        role_id="saifah_fe",
        payload={
            "description": "Implement Nuxt 3 frontend pages from UX specs",
            "depends_on": ["saas-ux"],
        },
    )
    be = TaskEnvelope(
        id="saas-be",
        type="implement_be",
        role_id="somsak_be",
        payload={
            "description": "Implement FastAPI backend endpoints and models",
            "depends_on": ["saas-pm"],
        },
    )
    qa = TaskEnvelope(
        id="saas-qa",
        type="test_qa",
        role_id="somjai_qa",
        payload={
            "description": "Run QA test suite against FE and BE deliverables",
            "depends_on": ["saas-fe", "saas-be"],
        },
        failure_policy=FailurePolicy.ESCALATE,
    )
    deploy = TaskEnvelope(
        id="saas-deploy",
        type="deploy",
        role_id="sombat_devops",
        payload={
            "description": "Build Docker images and prepare deployment config",
            "depends_on": ["saas-qa"],
        },
    )
    docs = TaskEnvelope(
        id="saas-docs",
        type="write_docs",
        role_id="somphop_docs",
        payload={
            "description": "Write user-facing documentation and API reference",
            "depends_on": ["saas-be", "saas-fe"],
        },
    )

    return build_plan(
        [pm, ux, fe, be, qa, deploy, docs],
        workflow_version=WORKFLOW_VERSION,
    )
