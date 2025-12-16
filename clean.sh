#!/usr/bin/env bash
set -euo pipefail

# This script cleans the project folder by removing the root repository links so agents can be used for anything.
# It removes leftover assets, metadata, and git state that would tie the copy to the original repo.
# It also removes framework-development artifacts that aren't needed for a reusable snapshot.
#
# Note: .codex-swarm/agentctl.md stays as part of the framework snapshot.

rm -rf \
  .DS_Store \
  .env* \
  .github \
  .gitattributes \
  .git \
  __pycache__ \
  .pytest_cache \
  .venv \
  assets \
  docs \
  README.md \
  tasks.html \
  LICENSE \
  tasks.json \
  CONTRIBUTING.md \
  CODE_OF_CONDUCT.md \
  GUIDELINE.md

# Recreate an empty tasks.json so the framework is usable after cleanup.
python - <<'PY' > tasks.json
import hashlib
import json

tasks = []
payload = json.dumps({"tasks": tasks}, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
checksum = hashlib.sha256(payload).hexdigest()

data = {
    "tasks": tasks,
    "meta": {
        "schema_version": 1,
        "managed_by": "agentctl",
        "checksum_algo": "sha256",
        "checksum": checksum,
    },
}

print(json.dumps(data, indent=2, ensure_ascii=False))
PY

# Initialize a fresh repository after the cleanup so the folder can be reused independently.
git init
git add .codex-swarm scripts .gitignore AGENTS.md tasks.json
git commit -m "Initial commit"

rm -rf clean.sh
