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

## Task Notes (legacy)

## Goal

- Remove duplication between `docs/workflow/T-###/README.md` and `docs/workflow/T-###/pr/description.md` by adopting a single canonical per-task folder layout under `docs/workflow/T-###/`.

## Scope

- Update `scripts/agentctl.py` to use the new layout by default:
  - Canonical task doc: `docs/workflow/T-###/README.md`
  - PR artifacts: `docs/workflow/T-###/pr/{meta.json,diffstat.txt,verify.log,review.md}`
  - Keep backward compatibility for reading existing old paths (`docs/workflow/T-###/README.md` and `docs/workflow/T-###/pr/*`) during the transition.
- Migrate existing tracked artifacts (tasks and PR folders) to the new layout.
- Update agent instructions and documentation to reference the new layout and stop mentioning the old `docs/workflow/prs/...` pipeline.

## Verification

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke:
  - `python scripts/agentctl.py pr check T-073`
  - `python scripts/agentctl.py verify T-073 --log docs/workflow/T-073/pr/verify.log --skip-if-unchanged`
