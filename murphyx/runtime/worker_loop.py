"""
Worker loop — dequeue tasks, bind role, execute, ack/nack.

Scaffold only. Implementation will connect queue + LLM client + role switcher.
Safe for public repo; no proprietary execution logic here.
"""

# TODO: Implement main loop — poll Redis (or in-proc queue), dispatch by role.


def run_worker_loop() -> None:
    """Entry point for local worker process — stub."""
    raise NotImplementedError("worker_loop.run_worker_loop — to be implemented")


if __name__ == "__main__":
    run_worker_loop()
