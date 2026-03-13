"""
Artifact store — paths for large outputs (code, docs, design).

Tasks must reference artifacts by path; payloads must not inline big blobs.
See artifacts/README.md and .cursorrules (Artifact store).
"""

import os
from pathlib import Path

# Repo root relative to this file: murphyx/services/ -> ../../artifacts
_DEFAULT_ROOT = Path(__file__).resolve().parent.parent.parent / "artifacts"


def _root_path() -> Path:
    override = os.getenv("ARTIFACTS_ROOT")
    return Path(override).resolve() if override else _DEFAULT_ROOT


def artifacts_root() -> Path:
    """Root directory for all task artifacts."""
    root = _root_path()
    root.mkdir(parents=True, exist_ok=True)
    return root


def task_artifact_dir(task_id: str) -> Path:
    """Per-task directory: artifacts/{task_id}/"""
    d = artifacts_root() / task_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def artifact_ref(task_id: str, *parts: str) -> str:
    """Stable ref string for task payload (posix path under artifacts/)."""
    return str(Path(task_id, *parts).as_posix())
