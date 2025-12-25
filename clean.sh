#!/usr/bin/env bash
set -euo pipefail

# Interactive workflow mode selection (direct vs branch_pr).
# - If CODEXSWARM_MODE is set, it wins.
# - If stdin is a TTY, we prompt.
# - Otherwise default to direct.
MODE="${CODEXSWARM_MODE:-}"
if [[ -z "${MODE}" && -t 0 ]]; then
  read -r -p "Select workflow_mode (direct/branch_pr) [direct]: " MODE || true
fi
MODE="${MODE:-direct}"
case "${MODE}" in
  direct|branch_pr) ;;
  *)
    echo "Invalid workflow_mode: ${MODE} (expected: direct or branch_pr)" >&2
    exit 2
    ;;
esac
export MODE

# This script cleans the project folder by removing the root repository links so agents can be used for anything.
# It removes leftover assets, metadata, and git state that would tie the copy to the original repo.
# It also removes framework-development artifacts (including docs/) that aren't needed for a reusable snapshot.
#
# Note: .codex-swarm/agentctl.md and .codex-swarm/workspace stay as part of the framework snapshot.

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
  scripts \
  README.md \
  tasks.html \
  LICENSE \
  .codex-swarm/tasks.json \
  CONTRIBUTING.md \
  CODE_OF_CONDUCT.md \
  GUIDELINE.md

# Recreate an empty tasks file so the framework is usable after cleanup.
python - <<'PY' > .codex-swarm/tasks.json
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

# Apply the selected workflow_mode and scrub agent prompts for the unused mode.
python - <<'PY'
import json
import os
import re
from pathlib import Path
from typing import Optional

ROOT = Path.cwd().resolve()
mode = os.environ.get("MODE", "").strip() or os.environ.get("CODEXSWARM_MODE", "").strip() or "direct"
if mode not in {"direct", "branch_pr"}:
    raise SystemExit(f"Invalid MODE: {mode!r}")

def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def simplify_mode_clause(text: str, keep: str) -> str:
    s = text
    if keep == "direct":
        if "in `branch_pr`" in s and "; in `direct`" in s:
            prefix, rest = s.split(": ", 1) if ": " in s else ("", s)
            direct_part = rest.split("; in `direct`", 1)[1]
            direct_part = direct_part.lstrip(" ,")
            return (prefix + ": " if prefix else "") + "in `direct`, " + direct_part
        if "In `direct`" in s and "branch_pr" in s:
            direct_sentence = s[s.index("In `direct`") :].strip()
            if s.startswith("Check ") and ":" in s:
                prefix = s.split(":", 1)[0] + ":"
                return prefix + " " + direct_sentence
            return direct_sentence
        return s

    if keep == "branch_pr":
        if "in `branch_pr`" in s and "; in `direct`" in s:
            prefix, rest = s.split(": ", 1) if ": " in s else ("", s)
            branch_part = rest.split("; in `direct`", 1)[0].strip()
            return (prefix + ": " if prefix else "") + branch_part
        if " In `direct`" in s and "branch_pr" in s:
            # Drop the direct sentence.
            return s.split(" In `direct`", 1)[0].rstrip(". ") + "."
        return s

    return s

def scrub_line(line: str) -> Optional[str]:
    s = (line or "").strip()
    if not s:
        return None

    if mode == "direct":
        s = simplify_mode_clause(s, keep="direct")
        if "`workflow_mode=branch_pr`" in s:
            return None
        if "`branch_pr`" in s and "`direct`" not in s:
            return None
        if "task branch" in s.lower() and "`direct`" not in s:
            return None
        if ".codex-swarm/worktrees" in s:
            return None
        if "integrate" in s and "In `direct`" not in s and "`direct`" not in s and "direct" not in s.lower():
            # Integrate is a branch_pr artifact flow; keep only if explicitly direct-scoped.
            return None
        if "--worktree" in s:
            s = s.replace("--worktree", "").replace("  ", " ").replace("  ", " ").strip()
            s = s.replace("  ", " ")
            s = s.replace("`python .codex-swarm/agentctl.py work start T-123 --agent <ROLE> --slug <slug>`", "`python .codex-swarm/agentctl.py work start T-123`")
            s = s.replace("`python .codex-swarm/agentctl.py work start T-123 --agent CODER --slug <slug>`", "`python .codex-swarm/agentctl.py work start T-123`")
        return s or None

    # branch_pr
    s = simplify_mode_clause(s, keep="branch_pr")
    if "`workflow_mode=direct`" in s:
        return None
    if "`direct`" in s and "`branch_pr`" not in s and "workflow_mode" not in s:
        return None
    if "no task branches/worktrees" in s.lower():
        return None
    return s or None

def scrub_json_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    for key in ["role", "description"]:
        if isinstance(data.get(key), str):
            new = scrub_line(data[key])
            if new is None:
                new = ""
            if new != data[key]:
                data[key] = new
                changed = True

    for key in ["inputs", "outputs", "permissions", "workflow"]:
        arr = data.get(key)
        if not isinstance(arr, list):
            continue
        new_arr = []
        for item in arr:
            if not isinstance(item, str):
                continue
            new = scrub_line(item)
            if new:
                new_arr.append(new)
        if new_arr != arr:
            data[key] = new_arr
            changed = True

    if changed:
        write_json(path, data)

def scrub_workflow_mode_docs(path: Path) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace").splitlines(True)
    out: list[str] = []
    skip = False
    remove_direct = (mode == "branch_pr")
    remove_branch_pr = (mode == "direct")

    def is_mode_header(line: str) -> Optional[str]:
        if line.startswith("- `direct`"):
            return "direct"
        if line.startswith("- `branch_pr`"):
            return "branch_pr"
        if re.match(r"^- `workflow_mode: \"?direct\"?`", line):
            return "direct"
        if re.match(r"^- `workflow_mode: \"?branch_pr\"?`", line):
            return "branch_pr"
        return None

    for line in text:
        header = is_mode_header(line.strip())
        if header == "direct":
            skip = remove_direct
        elif header == "branch_pr":
            skip = remove_branch_pr
        elif header is not None:
            skip = False
        if skip:
            continue
        out.append(line)
    Path(path).write_text("".join(out), encoding="utf-8")

# 1) Set the workflow mode in config.json
config_path = ROOT / ".codex-swarm" / "config.json"
config = json.loads(config_path.read_text(encoding="utf-8"))
config["workflow_mode"] = mode
write_json(config_path, config)

# 2) Scrub agent prompts
agents_dir = ROOT / ".codex-swarm" / "agents"
for agent_path in sorted(agents_dir.glob("*.json")):
    scrub_json_file(agent_path)

# 3) Scrub the two human-facing prompt docs
scrub_workflow_mode_docs(ROOT / "AGENTS.md")
scrub_workflow_mode_docs(ROOT / ".codex-swarm" / "agentctl.md")
PY

# Initialize a fresh repository after the cleanup so the folder can be reused independently.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # If we're already in a git repo, pin the current branch as the base branch for agentctl.
  current_branch="$(git symbolic-ref --short -q HEAD || true)"
  if [[ -n "${current_branch}" && "${current_branch}" != "HEAD" ]]; then
    git config --local codexswarm.baseBranch "${current_branch}"
  fi
else
  # Initialize a new git repo. Prefer `main` when supported.
  if git init -b main >/dev/null 2>&1; then
    :
  else
    git init
    git switch -c main >/dev/null 2>&1 || true
  fi

  current_branch="$(git symbolic-ref --short -q HEAD || true)"
  if [[ -n "${current_branch}" && "${current_branch}" != "HEAD" ]]; then
    git config --local codexswarm.baseBranch "${current_branch}"
  fi
fi

git add .codex-swarm .gitignore AGENTS.md
git commit -m "Initial commit"

rm -rf clean.sh
