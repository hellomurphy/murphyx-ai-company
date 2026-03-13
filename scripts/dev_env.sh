#!/usr/bin/env bash
# Dev tool — bootstrap local venv with editable install. No business logic.
set -e
cd "$(dirname "$0")/.."

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e ".[dev]"

echo "Done. Activate with: source .venv/bin/activate"
