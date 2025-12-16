# T-068: agentctl verify: log output + skip if unchanged

## Summary

- Add `agentctl verify --log` to append captured stdout+stderr into a PR-tracked `verify.log`.
- Add `--skip-if-unchanged` to avoid re-running verify when the current SHA matches `last_verified_sha`.

## Scope

- `scripts/agentctl.py`: extend `verify` CLI + enrich captured verify entries with `sha=...` / `verified_sha=...`; update PR `meta.json` with `last_verified_sha`/`last_verified_at` when available.
- `.codex-swarm/agentctl.md`: document the recommended verify invocation for PR artifacts.

## Risks

- If PR `meta.json` has a stale `head_sha`, `--skip-if-unchanged` will warn and may not skip until `pr update` runs.
- `verify.log` grows over time; it is expected to be append-only.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py verify T-068 --log docs/workflow/T-068/pr/verify.log`
- Re-run: `python scripts/agentctl.py verify T-068 --log docs/workflow/T-068/pr/verify.log --skip-if-unchanged`

## Rollback Plan

- Revert the task branch commit(s) or squash-merge revert on `main`.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.md`
- `docs/workflow/T-068/pr/description.md`
- `docs/workflow/T-068/pr/diffstat.txt`
- `docs/workflow/T-068/pr/meta.json`
- `docs/workflow/T-068/pr/review.md`
- `docs/workflow/T-068/pr/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->

## Task Notes (legacy)

## Goal

- Reduce manual PR bookkeeping and avoid redundant verify runs by enhancing `python scripts/agentctl.py verify` with optional logging and change detection.

## Scope

- `scripts/agentctl.py`:
  - Add `verify --log PATH` to append timestamped output per verify command (combined stdout+stderr).
  - Add `verify --skip-if-unchanged`:
    - If `--log` points under `docs/workflow/T-###/pr/`, treat PR `meta.json:head_sha` as the “current SHA”.
    - Otherwise treat `git rev-parse HEAD` (in `--cwd`) as the “current SHA”.
    - Skip running verify commands when `current_sha == last_verified_sha`.
  - After successful verify, persist `last_verified_sha` + `last_verified_at` in `docs/workflow/T-###/pr/meta.json` when available.
- Docs:
  - Update `.codex-swarm/agentctl.md` with the new `verify` options and the recommended “log to PR artifact” workflow.

## Verification

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke (branch_pr):
  - Run verify once: `python scripts/agentctl.py verify T-067 --log docs/workflow/T-067/pr/verify.log`
  - Re-run with `--skip-if-unchanged` and confirm it skips when the SHA is unchanged.
