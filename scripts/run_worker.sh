#!/usr/bin/env bash
# Dev tool — start the MurphyX worker loop. No business logic here.
set -e
cd "$(dirname "$0")/.."
exec .venv/bin/python -m murphyx.runtime.worker_loop
