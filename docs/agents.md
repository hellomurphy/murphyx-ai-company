# Agents

MurphyX agents follow the **Som-\*** Thai naming convention. Each agent is a thin wrapper that binds a **role_id** to a system prompt and tool allowlist, then delegates to the shared LLM client.

## Conventions

- **ROLE_ID** is a snake_case string (e.g. `somsak_be`) used everywhere: router, role switcher, prompt file name.
- **Prompts** live in `murphyx/prompts/{role_id}_prompt.txt` as plain text. Agent code must not inline long system prompts.
- **Stateless execution** — each task gets a clean `bind_role` / `unbind_role` cycle. No in-process state carries over between tasks.

## Role binding flow

1. Worker loop dequeues a `TaskEnvelope` with a `role_id` field.
2. `bind_role(role_id)` loads the prompt file and resolves the tool allowlist from the registry.
3. The LLM receives the system prompt + task payload and produces output.
4. `unbind_role()` marks the context boundary — no memory persists.

See `murphyx/runtime/role_switcher.py` for the implementation and `murphyx/orchestrator/task_router.py` for the task-type-to-role mapping.

## Task type routing

The router maps `task.type` to a `role_id`:

| Task type | Role ID |
|-----------|---------|
| `plan` | `somchai_pm` |
| `design_ux` | `somruedee_ux` |
| `implement_fe` | `saifah_fe` |
| `implement_be` | `somsak_be` |
| `test_qa` | `somjai_qa` |
| `deploy` | `sombat_devops` |
| `write_docs` | `somphop_docs` |
| `marketing_copy` | `somjit_marketing` |
| `sales_copy` | `somchok_sales` |
| `customer_success` | `somporn_cs` |
| `ceo_decompose` | `ceo` |

Unknown task types route to `__done__` (terminal state).

## Public repo note

Public examples implement a subset of the 15 roles defined in the README. The full roster exists in the internal agent roster; this repo provides framework-level implementations only.
