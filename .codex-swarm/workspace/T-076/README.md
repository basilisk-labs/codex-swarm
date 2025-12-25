# T-076: agentctl: verify auto-log to per-task pr/verify.log

## Summary

- Make `agentctl verify` auto-append to `.codex-swarm/workspace/T-###/pr/verify.log` when a PR artifact exists, so callers don’t need to pass `--log` every time.

## Goal

- Reduce friction for verification logging in `workflow_mode=branch_pr` while keeping `--log` as an explicit override.

## Scope

- `scripts/agentctl.py`: default verify log path selection when `--log` is not provided.
- `.codex-swarm/agentctl.md`: document the new default.

## Risks

- Auto-logging could surprise users who expected no file writes; limited to cases where a tracked PR `verify.log` already exists.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke:
  - `python scripts/agentctl.py pr open T-076 --author CODER --branch task/T-076/verify-auto-log`
  - `python scripts/agentctl.py verify T-076` (should append to `.codex-swarm/workspace/T-076/pr/verify.log`)

## Rollback Plan

- Revert this task commit(s); `agentctl verify --log ...` remains supported.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
