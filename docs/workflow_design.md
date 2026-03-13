# Workflow design

## Router / FSM pattern

Control flow in MurphyX follows a Router/FSM model (Pillar 1 in `.cursorrules`). The worker loop only dequeues; the router decides what happens next.

```mermaid
flowchart TD
    Queue[Task Queue] -->|dequeue| Worker[Worker Loop]
    Worker -->|bind_role| RoleSwitcher[Role Switcher]
    RoleSwitcher -->|system prompt + tools| LLM[LLM Client]
    LLM -->|output| ArtifactStore[Artifact Store]
    Worker -->|ack/nack| Queue
    Worker -->|route_task| Router[Task Router]
    Router -->|next role_id| Worker
```

## Task lineage

Every task carries lineage fields for traceability:

```mermaid
flowchart LR
    Goal[Founder Goal] -->|CEO decompose| T1[Task A]
    Goal --> T2[Task B]
    T1 -->|parent_task_id| T3[Subtask A.1]
    T2 -->|parent_task_id| T4[Subtask B.1]
    T1 -.->|workflow_id| WF[Workflow abc123]
    T2 -.->|workflow_id| WF
    T3 -.->|workflow_id| WF
    T4 -.->|workflow_id| WF
```

Fields: `task_id`, `parent_task_id`, `workflow_id`, `workflow_version`.

## Build SaaS workflow graph

```mermaid
flowchart TD
    PM[PM: plan] --> UX[UX: design]
    PM --> BE[BE: implement]
    UX --> FE[FE: implement]
    FE --> QA[QA: test]
    BE --> QA
    QA --> Deploy[DevOps: deploy]
    FE --> Docs[Docs: write]
    BE --> Docs
```

## Failure handling

Each task declares a `FailurePolicy`:

- **retry** — re-enqueue up to `max_retries` times
- **escalate** — move to dead-letter queue for human review
- **abort** — stop the workflow immediately

The worker loop applies this policy automatically on task failure.

## Versioning

Workflows set `workflow_version` on all tasks they produce. When you change a workflow's task structure, bump the version so workers can distinguish old-format tasks from new ones.
