# T-074: Unify workflow artifact layout (single per-task folder)

## Summary

- Unify workflow documentation + PR artifacts under a single per-task directory (`docs/workflow/T-###/`) to remove duplication and reduce navigation friction.

## Scope

- Update `scripts/agentctl.py` to use the new per-task artifact layout by default and remain compatible with existing old paths during migration.
- Migrate existing tracked artifacts from:
  - `docs/workflow/T-###/README.md` → `docs/workflow/T-###/README.md`
  - `docs/workflow/T-###/pr/*` → `docs/workflow/T-###/pr/*`
- Update `AGENTS.md`, `.codex-swarm/agents/*.json`, `.codex-swarm/agentctl.md`, and repo docs to reference the new layout.

## Risks

- Path migration touches many files and can break scripts if any path assumptions remain.
- Temporary coexistence of old/new paths during the transition could confuse contributors if docs are not updated consistently.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py pr check T-073` (after migration)

## Rollback Plan

- Revert the merge commit(s) for T-074; old artifacts remain in git history and can be restored.
- If needed, re-introduce the `docs/workflow/prs/` layout and re-point `agentctl` path helpers back to the legacy locations.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
