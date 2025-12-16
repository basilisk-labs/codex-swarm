# T-073: Reduce integrate noise: auto-sync PR meta head_sha

## Summary

- Reduce integrate noise by treating task branch HEAD as authoritative and ensuring PR `meta.json` is corrected on `main` after integration.

## Scope

- `scripts/agentctl.py`: update `integrate` to avoid warning spam when PR meta `head_sha` is stale; write correct `head_sha` and `last_verified_sha` into `docs/workflow/prs/T-073/meta.json` on `main` after merge.

## Risks

- Minimal; behavior change is mostly output and PR meta bookkeeping.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: integrate a branch with stale PR meta and confirm no warning is emitted and `meta.json` on main is corrected.

## Rollback Plan

- Revert the task branch / squash merge.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
