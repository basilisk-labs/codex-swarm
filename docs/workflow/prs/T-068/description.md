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
- `python scripts/agentctl.py verify T-068 --log docs/workflow/prs/T-068/verify.log`
- Re-run: `python scripts/agentctl.py verify T-068 --log docs/workflow/prs/T-068/verify.log --skip-if-unchanged`

## Rollback Plan

- Revert the task branch commit(s) or squash-merge revert on `main`.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.md`
- `docs/workflow/prs/T-068/description.md`
- `docs/workflow/prs/T-068/diffstat.txt`
- `docs/workflow/prs/T-068/meta.json`
- `docs/workflow/prs/T-068/review.md`
- `docs/workflow/prs/T-068/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->
