# MurphyX — Quickstart Testing (single-agent, light mode)

## Goal

Verify that the **core runtime + prompts + LLM client** work end-to-end with **minimal load**.  
This path uses **one agent** and **a single LLM call** — ideal for validating the pipeline before running full workflows, workers, and APIs.

Recommended flow (what most devs will try first):

1. Create a virtualenv and install dependencies (once)
2. For every new session, **ALWAYS activate the venv first**
3. Start the LLM (Ollama)
4. Run the single-agent demo script

---

## 1. One-time setup

From the repo root:

```bash
git clone https://github.com/your-org/murphyx-ai-company.git
cd murphyx-ai-company

# create virtualenv and install dependencies
./scripts/dev_env.sh

# copy example environment
cp .env.example .env
```

The default `.env` assumes:

- `LLM_PROVIDER=ollama`
- `LLM_BASE_URL=http://localhost:11434`
- `LLM_MODEL=llama3.2`
- `REDIS_URL=redis://localhost:6379/0`

You can change the model name later if you want a smaller/faster one, but
make sure `.env` and Ollama use the **same** model name.

---

## 2. Per-session rule: ALWAYS activate the env first

Every new terminal session:

```bash
cd /path/to/murphyx-ai-company
source .venv/bin/activate
```

Recommended helper in your shell profile (e.g. `~/.zshrc`):

```bash
alias workon_murphyx='cd /path/to/murphyx-ai-company && source .venv/bin/activate'
```

Then you can simply run:

```bash
workon_murphyx
```

---

## 3. Start the LLM (Ollama)

1. Install Ollama from `https://ollama.com/` (once)
2. In a separate terminal:

```bash
ollama serve
```

3. Pull the model (once per model):

```bash
ollama pull llama3.2
```

If you change `LLM_MODEL` in `.env`, use the same name when you run `ollama pull`.

---

## 4. Run the single-agent demo (lightest end-to-end test)

Back in the terminal where the venv is active:

```bash
workon_murphyx    # หรือ: cd ... && source .venv/bin/activate

.venv/bin/python examples/run_single_agent.py
```

### What happens under the hood

- A `TaskEnvelope` is created for the backend role (`somsak_be`)
- `bind_role` loads the system prompt and tool allowlist
- The LLM is called once via `murphyx.services.llm_client.complete()`
- The output is written to `artifacts/{task_id}/output.txt`

### How to check that it worked

- Inspect logs printed to stdout:
  - `murphyx.runtime.*`
  - `murphyx.role_switcher.*`
- Inspect the `artifacts/` directory:
  - There should be a new folder named after `task_id` containing `output.txt`

If both logs and artifacts look good, then:

- The **framework core** is functioning correctly (role switcher, runtime, artifact store)
- The **LLM integration** is healthy (httpx → Ollama)

From here, you can gradually move to heavier tests, such as:

- `examples/run_saas_builder.py` (build_saas workflow)
- `examples/run_company.py` (CEO decompose goal → plan → enqueue)
- And later the full worker + Redis + API flows described in `README.md`

