# T-073: Reduce integrate noise: auto-sync PR meta head_sha

## Summary

- Reduce integrate noise by treating task branch HEAD as authoritative and ensuring PR `meta.json` is corrected on `main` after integration.

## Scope

- `scripts/agentctl.py`: update `integrate` to avoid warning spam when PR meta `head_sha` is stale; write correct `head_sha` and `last_verified_sha` into `docs/workflow/T-073/pr/meta.json` on `main` after merge.

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

## Task Notes (legacy)

## Goal

- Speed up the local branch_pr pipeline by removing the common `integrate` warning about stale PR `meta.json` `head_sha`, while keeping PR artifacts accurate on `main`.

## Scope

- `scripts/agentctl.py`:
  - During `integrate`, treat the task branch HEAD SHA as authoritative (instead of warning).
  - After merge, ensure `docs/workflow/T-###/pr/meta.json` on `main` reflects the correct `head_sha` and `last_verified_sha` for the integrated branch head.
- No changes to task branches (single-writer PR artifacts remain owned by the task branch until merge).

## Verification

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: run `integrate` on a task branch whose PR `meta.json` is stale and confirm no warning is emitted and the merged PR `meta.json` is corrected on `main`.
