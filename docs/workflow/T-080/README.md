# T-080: agentctl: integrate auto-updates PR diffstat + README auto-summary

## Summary

- Auto-refresh `docs/workflow/T-###/pr/diffstat.txt` and the README auto-summary during `agentctl integrate` so reviewers don’t need to run `pr update` manually.

## Goal

- Remove the manual “run `pr update` before review/integrate” step by having `integrate` refresh PR artifacts on `main` after merge.

## Scope

- `scripts/agentctl.py`:
  - After merge, regenerate `docs/workflow/T-###/pr/diffstat.txt`.
  - After merge, update `docs/workflow/T-###/README.md` auto-summary block (between `<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->`) when present.
- `.codex-swarm/agentctl.md`: document the automatic refresh.

## Risks

- Minimal, but touches files during `integrate` (changes are committed as part of the closure commit on `main`).

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: run `integrate` for a task branch without running `pr update` first and confirm diffstat + README auto-summary are refreshed on `main`.

## Rollback Plan

- Revert the task changes; `integrate` falls back to existing behavior and executors can keep running `pr update` manually.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.md`
- `docs/workflow/T-080/README.md`
- `docs/workflow/T-080/pr/diffstat.txt`
- `docs/workflow/T-080/pr/meta.json`
- `docs/workflow/T-080/pr/review.md`
- `docs/workflow/T-080/pr/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->
