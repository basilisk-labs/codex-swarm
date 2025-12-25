# T-074: Unify workflow artifact layout (single per-task folder)

## Summary

- Unify workflow documentation + PR artifacts under a single per-task directory (`.codex-swarm/workspace/T-###/`) to remove duplication and reduce navigation friction.

## Scope

- Update `scripts/agentctl.py` to use the new per-task artifact layout by default and remain compatible with existing old paths during migration.
- Migrate existing tracked artifacts from:
  - `.codex-swarm/workspace/T-###/README.md` → `.codex-swarm/workspace/T-###/README.md`
  - `.codex-swarm/workspace/T-###/pr/*` → `.codex-swarm/workspace/T-###/pr/*`
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
- If needed, re-introduce the `.codex-swarm/workspace/prs/` layout and re-point `agentctl` path helpers back to the legacy locations.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

## Task Notes (legacy)

## Goal

- Remove duplication between `.codex-swarm/workspace/T-###/README.md` and `.codex-swarm/workspace/T-###/pr/description.md` by adopting a single canonical per-task folder layout under `.codex-swarm/workspace/T-###/`.

## Scope

- Update `scripts/agentctl.py` to use the new layout by default:
  - Canonical task doc: `.codex-swarm/workspace/T-###/README.md`
  - PR artifacts: `.codex-swarm/workspace/T-###/pr/{meta.json,diffstat.txt,verify.log,review.md}`
  - Keep backward compatibility for reading existing old paths (`.codex-swarm/workspace/T-###/README.md` and `.codex-swarm/workspace/T-###/pr/*`) during the transition.
- Migrate existing tracked artifacts (tasks and PR folders) to the new layout.
- Update agent instructions and documentation to reference the new layout and stop mentioning the old `.codex-swarm/workspace/prs/...` pipeline.

## Verification

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke:
  - `python scripts/agentctl.py pr check T-073`
  - `python scripts/agentctl.py verify T-073 --log .codex-swarm/workspace/T-073/pr/verify.log --skip-if-unchanged`
