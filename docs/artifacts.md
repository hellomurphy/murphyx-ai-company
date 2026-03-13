# Artifacts

Large agent outputs live under **`artifacts/`** at repo root—not inside task payloads. Task envelopes hold **refs only**.

Layout: `artifacts/{task_id}/...` — see `murphyx.services.artifact_store`.

**Git:** `artifacts/*` is ignored except `.gitkeep`—runtime output must not be committed.
