# T-075: agentctl: add work start (branch+pr+scaffold)

## Summary

- Add `agentctl work start` to create a task checkout (branch+worktree) and initialize per-task artifacts in one command.

## Goal

- Reduce the number of manual setup steps for `workflow_mode=branch_pr` so starting a task is fast and consistent.

## Scope

- `scripts/agentctl.py`:
  - Add `work start` that orchestrates `branch create` + `task scaffold` + `pr open/update` inside the new worktree.
  - Keep behavior idempotent via `--reuse` and optional doc overwrite via `--overwrite`.
- `.codex-swarm/agentctl.md`: document the new command.

## Risks

- Running subprocesses in another checkout can hide errors if output is swallowed; `work start` fails hard on non-zero exit and surfaces stdout/stderr.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py work start --help`

## Rollback Plan

- Revert the task commit(s); the existing `branch/pr/task scaffold` commands remain unchanged.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.md`
- `.codex-swarm/workspace/T-075/README.md`
- `.codex-swarm/workspace/T-075/pr/diffstat.txt`
- `.codex-swarm/workspace/T-075/pr/meta.json`
- `.codex-swarm/workspace/T-075/pr/review.md`
- `.codex-swarm/workspace/T-075/pr/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->
