"""
Circuit breaker — disable a tool temporarily after N consecutive failures.
"""

from __future__ import annotations

import time

from murphyx.observability import get_logger, log_event

logger = get_logger("circuit_breaker")


class CircuitBreaker:
    """Per-tool breaker. Open after threshold fails; resets after cooldown."""

    def __init__(self, name: str, threshold: int = 10, cooldown_sec: float = 60.0):
        self.name = name
        self.threshold = threshold
        self.cooldown_sec = cooldown_sec
        self._fail_count = 0
        self._opened_at: float | None = None

    @property
    def is_open(self) -> bool:
        if self._opened_at is None:
            return False
        if time.monotonic() - self._opened_at >= self.cooldown_sec:
            self.reset()
            return False
        return True

    def record_success(self) -> None:
        self._fail_count = 0
        self._opened_at = None

    def record_failure(self) -> None:
        self._fail_count += 1
        if self._fail_count >= self.threshold:
            self._opened_at = time.monotonic()
            log_event(
                logger, "breaker_open",
                tool=self.name, fails=self._fail_count, cooldown=self.cooldown_sec,
            )

    def reset(self) -> None:
        self._fail_count = 0
        self._opened_at = None
        log_event(logger, "breaker_reset", tool=self.name)
