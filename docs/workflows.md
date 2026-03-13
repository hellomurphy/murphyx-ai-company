# Workflows

Workflows produce ordered `list[TaskEnvelope]` for the queue. Each workflow assigns a shared `workflow_id` and `workflow_version` to its tasks via the planner's topological sort.

All implementations live in `murphyx/workflows/`.

---

## build_saas

**File:** `murphyx/workflows/build_saas.py`
**Version:** `1`
**Tasks:** 7

Pipeline: PM -> UX -> FE + BE (parallel after PM) -> QA -> Deploy -> Docs.

```
saas-pm (plan)
  └─ saas-ux (design_ux)
       └─ saas-fe (implement_fe)
  └─ saas-be (implement_be)
            └─ saas-qa (test_qa)  [depends on FE + BE]
                  └─ saas-deploy (deploy)
       └─ saas-docs (write_docs) [depends on FE + BE]
```

Usage:

```python
from murphyx.workflows.build_saas import create_build_saas_tasks

tasks = create_build_saas_tasks("Pet grooming SaaS MVP")
# Returns 7 TaskEnvelopes in topological order
```

QA uses `FailurePolicy.ESCALATE` — failures bubble up to the PM rather than silent retry.

---

## qa_pipeline

**File:** `murphyx/workflows/qa_pipeline.py`
**Version:** `1`

Creates one QA task per artifact ref. Each task uses `FailurePolicy.RETRY` with `max_retries=2`.

```python
from murphyx.workflows.qa_pipeline import enqueue_qa_pipeline

ids = await enqueue_qa_pipeline(["task123/output.txt", "task456/output.txt"])
```

---

## deploy_pipeline

**File:** `murphyx/workflows/deploy_pipeline.py`
**Version:** `1`
**Tasks:** 2

1. `deploy-build` — build Docker images (`FailurePolicy.ABORT`)
2. `deploy-health` — run health checks (`FailurePolicy.ESCALATE`, depends on build)

```python
from murphyx.workflows.deploy_pipeline import enqueue_deploy_pipeline

ids = await enqueue_deploy_pipeline(["ref/output.txt"])
```

---

## Versioning

All workflows set `workflow_version` on every task. When workflow logic changes, increment the version string to ensure compatibility with already-queued tasks from the previous version.

## Execution budget

Workflows respect the execution budget defined in `.cursorrules`. The worker loop enforces `MAX_STEPS` (default 1000) to prevent infinite loops.
