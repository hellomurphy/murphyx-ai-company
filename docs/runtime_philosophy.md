# Runtime philosophy

Short rule -> follow. Pillars in `.cursorrules`; long form in `docs/architecture.md`.

## Core principles and implementations

### Artifact store

Large agent outputs (generated code, docs, design specs) are stored in `artifacts/{task_id}/` — never inlined in task payloads. Task envelopes carry `artifact_refs` (path strings) only.

Implementation: `murphyx/services/artifact_store.py` — `task_artifact_dir(task_id)` creates and returns the per-task directory. Configurable via `ARTIFACTS_ROOT` env var.

### Idempotency

Task handlers must be idempotent. The queue uses `ack` / `nack` semantics — a crashed worker causes re-delivery, and the handler must not produce duplicate side effects.

Implementation: `murphyx/queue/redis_queue.py` — `nack()` increments `retry_count` and checks `should_retry()` before re-enqueuing. Tasks that exceed `max_retries` go to a dead-letter queue.

The `write_file` tool (`murphyx/tools/filesystem/write_file.py`) is idempotent by design — it compares content hashes before writing and skips unchanged files.

### Circuit breaker

Tools that hit external services can fail repeatedly. A circuit breaker disables a tool after N consecutive failures and auto-resets after a cooldown period.

Implementation: `murphyx/tools/circuit_breaker.py` — `CircuitBreaker` class tracks fail count per tool. Used by `murphyx/tools/network/http_fetch.py`.

### Tool sandboxing

No unrestricted shell. No `eval` on LLM output. Tools run within controlled execution boundaries:

- **Filesystem tools** use path allowlists (only files under `cwd`)
- **Calculator** uses AST-based evaluation (no `eval()`)
- **Network tools** use URL allowlists + timeouts
- All tools run with `asyncio.wait_for` timeouts

Implementation: `murphyx/tools/base.py` — `run_with_timeout()` wrapper. Per-tool sandbox rules in each tool module.

### Stateless agents

Agent memory must not persist across tasks. Every `bind_role` / `unbind_role` cycle is a clean slate. Persistent state is read/written via queue or storage tools only.

Implementation: `murphyx/runtime/role_switcher.py` — `bind_role()` loads a fresh `RoleContext` from disk each time.

### Structured logging

All agent decisions, router transitions, tool calls, and outputs emit structured JSON logs.

Implementation: `murphyx/observability/__init__.py` — `get_logger(name)` returns a JSON-formatted logger under the `murphyx.*` namespace. `log_event(logger, msg, **kwargs)` emits structured fields.
