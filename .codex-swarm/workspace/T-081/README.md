# T-081: agentctl integrate: skip verify if already verified

## Summary

- Skip redundant `agentctl integrate` verify runs when the task branch SHA is already verified (PR meta `last_verified_sha` or `.codex-swarm/workspace/T-###/pr/verify.log`), while keeping `--run-verify` to force reruns.

## Goal

- Make `integrate` faster in the common case where CODER already ran `agentctl verify` and committed the updated `pr/verify.log`.

## Scope

- `scripts/agentctl.py`: detect “already verified” SHA and skip creating/using a verify worktree unless forced.
- `.codex-swarm/agentctl.md`: document the new behavior and the `--run-verify` escape hatch.

## Risks

- Skipping verify trusts previously recorded verification for the same SHA; mitigated by requiring an exact SHA match and providing `--run-verify` to force reruns.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: run `agentctl verify T-081` on the task branch (writes `.codex-swarm/workspace/T-081/pr/verify.log`), then run `agentctl integrate T-081 ...` on `main` and confirm verify is skipped unless `--run-verify` is passed.

## Rollback Plan

- Revert the task changes; `integrate` reverts to always running verify when commands exist.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.md`
- `.codex-swarm/workspace/T-081/README.md`
- `.codex-swarm/workspace/T-081/pr/diffstat.txt`
- `.codex-swarm/workspace/T-081/pr/meta.json`
- `.codex-swarm/workspace/T-081/pr/review.md`
- `.codex-swarm/workspace/T-081/pr/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->
