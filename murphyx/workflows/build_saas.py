"""
Build SaaS workflow — PM → design → FE → BE → QA → DevOps → docs.

Example automation only; no proprietary product logic.
"""

# TODO: Define ordered list of role steps and enqueue pattern.
WORKFLOW_STEPS = [
    "somchai_pm",
    "somying_frontend",
    "somsak_backend",
    # "qa", "devops", "writer" — add when agent modules exist
]


def enqueue_build_saas(goal: str) -> None:
    """Enqueue full pipeline — stub."""
    raise NotImplementedError
