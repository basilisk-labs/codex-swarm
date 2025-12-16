# T-070: agentctl guard commit: add --auto-allow

## Summary

- Add `--auto-allow` to `python scripts/agentctl.py guard commit` so it can infer an allowlist from staged files (matching the existing `agentctl commit --auto-allow` behavior).

## Scope

- `scripts/agentctl.py`: extend `guard commit` parser + flow to derive `--allow` from staged files when `--auto-allow` is set.
- `.codex-swarm/agentctl.md`: document the recommended usage.

## Risks

- None expected; `--auto-allow` is opt-in and does not change behavior when explicit `--allow` is provided.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: stage a small change and run `python scripts/agentctl.py guard commit T-070 -m \"...\" --auto-allow`.

## Rollback Plan

- Revert this task branch.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
