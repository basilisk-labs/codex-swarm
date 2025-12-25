# T-077: agentctl: cleanup merged task branches/worktrees

## Summary

- Add `agentctl cleanup merged` to remove merged `task/*` branches and their `.codex-swarm/worktrees/*` checkouts safely (dry-run by default).

## Goal

- Reduce manual repo hygiene work after tasks are integrated and closed.

## Scope

- `scripts/agentctl.py`: new `cleanup merged` command that selects only DONE tasks whose branch diff vs `main` is empty.
- `.codex-swarm/agentctl.md`: document usage.

## Risks

- False positives could delete a branch that still matters; mitigated by requiring `DONE` + empty `git diff main...branch` and `--yes` for deletion.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke:
  - `python scripts/agentctl.py cleanup merged` (dry-run)

## Rollback Plan

- Recreate the deleted task branch from git history if needed; worktree removal does not delete commits.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
