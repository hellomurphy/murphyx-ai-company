# Observability

Structured JSON logging for all agent decisions, router transitions, tool calls, and outputs per `.cursorrules`.

## API

### `get_logger(name: str) -> logging.Logger`

Returns a child logger under `murphyx.*` with JSON output to stderr. Reads `LOG_LEVEL` from Settings on first call.

```python
from murphyx.observability import get_logger

logger = get_logger("my_module")
logger.info("something happened")
# {"ts": "...", "level": "INFO", "logger": "murphyx.my_module", "msg": "something happened"}
```

### `log_event(logger, msg: str, **kwargs)`

Emit a structured log line with arbitrary key-value fields alongside the message.

```python
from murphyx.observability import get_logger, log_event

logger = get_logger("queue")
log_event(logger, "enqueued", task_id="abc123", queue="murphyx:tasks")
# {"ts": "...", "level": "INFO", "logger": "murphyx.queue", "msg": "enqueued", "task_id": "abc123", "queue": "murphyx:tasks"}
```

## Configuration

Set `LOG_LEVEL` in `.env` to control verbosity: `debug`, `info`, `warning`, `error`.
