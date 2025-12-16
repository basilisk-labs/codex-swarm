# T-079: Docs: remove remaining legacy prs/ mentions

## Summary

- Remove remaining “current” mentions of the legacy `docs/workflow/prs/` layout from workflow docs (keeping only clearly marked legacy references).

## Goal

- Reduce confusion after the T-074 migration by making documentation consistently point at `docs/workflow/T-###/` and `docs/workflow/T-###/pr/`.

## Scope

- Update workflow docs that still mention legacy `docs/workflow/prs/...` as a primary location.
- Do not rewrite historical task text inside `tasks.json`.

## Risks

- Minimal; doc-only edits.

## Verify Steps

- `python scripts/agentctl.py task lint`
- `rg -n \"docs/workflow/prs\" -S .` (remaining matches should be in legacy notes or historical diffstat snapshots)

## Rollback Plan

- Revert this task commit(s).

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
