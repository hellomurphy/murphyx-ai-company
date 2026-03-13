# Agent roles

All roles live under `murphyx/agents/`. Prompt files are in `murphyx/prompts/`.

## Role mapping

| Role ID | Agent name | Prompt file | Tools | Module |
|---------|-----------|-------------|-------|--------|
| `somchai_pm` | Somchai (PM) | `somchai_pm_prompt.txt` | — | `agents/somchai_pm.py` |
| `somruedee_ux` | Somruedee (UX) | `somruedee_ux_prompt.txt` | — | — |
| `saifah_fe` | Saifah (FE) | `frontend_prompt.txt` | `read_file`, `write_file` | `agents/somying_frontend.py` |
| `somsak_be` | Somsak (BE) | `backend_prompt.txt` | `read_file`, `write_file` | `agents/somsak_backend.py` |
| `somjai_qa` | Somjai (QA) | `somjai_qa_prompt.txt` | `read_file` | — |
| `sombat_devops` | Sombat (DevOps) | `sombat_devops_prompt.txt` | — | — |
| `somphop_docs` | Somphop (Docs) | `somphop_docs_prompt.txt` | `read_file` | — |
| `somjit_marketing` | Somjit (Marketing) | `marketing_prompt.txt` | — | `agents/somjit_marketing.py` |
| `somchok_sales` | Somchok (Sales) | `somchok_sales_prompt.txt` | — | — |
| `somporn_cs` | Somporn (CS) | `somporn_cs_prompt.txt` | — | `agents/somporn_customer_success.py` |
| `ceo` | Jarvis (CEO) | `ceo_prompt.txt` | — | `orchestrator/ceo_agent.py` |

## How binding works

`role_switcher.bind_role(role_id)` resolves the prompt file using two candidate paths:

1. `murphyx/prompts/{role_id}_prompt.txt`
2. `murphyx/prompts/{first_segment}_prompt.txt` (fallback for compound IDs)

If neither file exists, a generic fallback prompt is used. The tool allowlist is defined in `ROLE_TOOLS` inside `murphyx/runtime/role_switcher.py` and filtered against the live tool registry.

## Extending with new roles

1. Add the role_id to `ROLE_TOOLS` in `role_switcher.py`.
2. Add the task type mapping to `TASK_TYPE_TO_ROLE` in `task_router.py`.
3. Create a prompt file at `murphyx/prompts/{role_id}_prompt.txt`.
4. Optionally create an agent module in `murphyx/agents/`.
