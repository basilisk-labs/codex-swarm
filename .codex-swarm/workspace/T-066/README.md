# T-066: Branch workflow: task branches + worktrees + local PR artifacts

## Goal

- Enable real parallel agent work via task branches + git worktrees (kept inside this repo).
- Prevent `tasks.json` conflicts by enforcing “write only on `main`” and a dedicated INTEGRATOR role for closure.
- Provide a local PR-like flow without GitHub/GitLab: review + integration driven by tracked PR artifacts.

## Scope

- `agentctl`:
  - Add `branch` commands to create/remove task branches and worktrees under `.codex-swarm/worktrees/`.
  - Add `pr` commands to create/update/check tracked PR artifacts under `.codex-swarm/workspace/T-###/pr/`.
  - Add `integrate` to gate merges into `main` (with optional verify) and to enforce PR + single-writer rules.
  - Strengthen git guardrails to reject `tasks.json` changes outside `main`.
- Repo structure + docs:
  - Track PR artifacts under `.codex-swarm/workspace/T-###/pr/` and ignore `.codex-swarm/worktrees/` (legacy `.codex-swarm/workspace/prs/` is deprecated).
  - Introduce a new `INTEGRATOR` agent definition and update agent workflows to use branches/worktrees/PR artifacts.
  - Update `AGENTS.md` and `.codex-swarm/agentctl.md` with the new branching workflow.

## Non-goals

- No remote hosting integration (GitHub/GitLab), no network-dependent PR tooling.
- No automatic deletion of branches/worktrees without an explicit user prompt (cleanup remains manual/safe).

## Verification

- `python scripts/agentctl.py task lint`
- `python -m compileall scripts/agentctl.py`
- Smoke check help output: `python scripts/agentctl.py --help` and `python scripts/agentctl.py pr --help`

## Implementation notes

- Added `agentctl` commands:
  - `branch create/remove` for task branches + git worktrees under `.codex-swarm/worktrees/` (inside-repo only).
  - `pr open/update/check` for tracked PR artifacts under `.codex-swarm/workspace/T-###/pr/`.
  - `integrate` for gated merges into `main` (PR check + optional verify capture + squash/merge strategy).
- Enforced “single-writer tasks.json”:
  - `agentctl` refuses tasks.json writes unless running from the repo root checkout on `main`.
  - `agentctl guard commit` refuses committing `tasks.json` from a task worktree checkout or outside `main`.
- Added a new agent `INTEGRATOR` as the only role that merges into `main` and runs `finish` for task closure.

## Files touched

- `scripts/agentctl.py`
- `AGENTS.md`
- `.codex-swarm/agentctl.md`
- `.codex-swarm/agents/INTEGRATOR.json`
- `.codex-swarm/agents/CODER.json`
- `.codex-swarm/agents/TESTER.json`
- `.codex-swarm/agents/DOCS.json`
- `.codex-swarm/agents/PLANNER.json`
- `.codex-swarm/agents/REVIEWER.json`
- `.gitignore`
- `.codex-swarm/workspace/prs/README.md` (legacy)
- `.codex-swarm/workspace/README.md`
