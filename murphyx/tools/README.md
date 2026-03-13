# Tools

Sandboxed tools with Pydantic I/O schemas, `asyncio.wait_for` timeouts, and circuit breaker support.

- `filesystem/read_file.py` — path-allowlisted file reading
- `filesystem/write_file.py` — idempotent writes (content hash check)
- `compute/calculator.py` — AST-based safe arithmetic (no `eval`)
- `network/http_fetch.py` — URL-allowlisted HTTP GET with circuit breaker

Supporting modules:

- `base.py` — `run_with_timeout()` wrapper and `ToolResult` model
- `circuit_breaker.py` — per-tool breaker (fail count -> cooldown)
- `registry.py` — tool name -> module lookup for role switcher

See `.cursorrules` for tool contract, purity, and sandboxing rules.
