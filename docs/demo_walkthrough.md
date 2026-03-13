# Demo walkthrough

## Quick-start scripts

Run these from the repo root after setting up the environment (`scripts/dev_env.sh`):

1. **Single agent** — execute one task with a specific role:

   ```bash
   python examples/run_single_agent.py
   ```

2. **SaaS builder workflow** — enqueue the full build_saas pipeline:

   ```bash
   python examples/run_saas_builder.py
   ```

3. **Full company** — CEO decomposes a goal, then worker processes all tasks:

   ```bash
   python examples/run_company.py "Build a pet grooming SaaS MVP"
   ```

## Flagship demo app

`apps/pet-grooming-saas/` — a Nuxt 3 + FastAPI scaffold showing the output shape a MurphyX workflow produces.

```bash
cd apps/pet-grooming-saas
docker compose up
# API on http://localhost:8001
```

## Prerequisites

- Redis running locally (`scripts/start_redis.sh`)
- LLM provider configured in `.env` (defaults to Ollama on localhost:11434)
- Python venv with dependencies (`scripts/dev_env.sh`)
