"""
Observability — structured JSON logger.

All agent decisions, router transitions, tool calls, and outputs must use
get_logger() instead of print(). Reads LOG_LEVEL from Settings.
"""

import logging
import json
import sys
from typing import Any


class _JsonFormatter(logging.Formatter):
    """Emit each log record as a single JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, Any] = {
            "ts": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0] is not None:
            entry["exc"] = self.formatException(record.exc_info)
        extra = getattr(record, "_extra", None)
        if extra:
            entry.update(extra)
        return json.dumps(entry, default=str)


_CONFIGURED = False


def _configure_root(level: str = "INFO") -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_JsonFormatter())
    root = logging.getLogger("murphyx")
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under 'murphyx' with JSON output."""
    from murphyx.config import get_settings

    _configure_root(get_settings().log_level)
    return logging.getLogger(f"murphyx.{name}")


def log_event(logger: logging.Logger, msg: str, **kwargs: Any) -> None:
    """Convenience: emit structured key=value fields alongside a message."""
    record = logger.makeRecord(
        logger.name, logging.INFO, "(murphyx)", 0, msg, (), None
    )
    record._extra = kwargs  # type: ignore[attr-defined]
    logger.handle(record)
