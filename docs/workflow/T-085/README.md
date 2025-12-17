# T-085: agentctl work start: idempotent scaffold

## Summary

- Make `python scripts/agentctl.py work start` idempotent in `branch_pr`: don’t fail when the task README already exists in a newly created worktree.

## Goal

- Remove frequent `File already exists: .../docs/workflow/T-###/README.md` errors and make `work start` safe to use as the default entrypoint (as agents now recommend).

## Scope

- `scripts/agentctl.py`: in `cmd_work_start`, only run `task scaffold` when `docs/workflow/T-###/README.md` is missing, unless `--overwrite` is provided.

## Risks

- Low. Behavior change is limited to `work start` scaffolding logic.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: create a new task with a planning commit, then run `agentctl work start ...` twice; both runs should succeed without `--overwrite`.

## Rollback Plan

- Revert the change; `work start` reverts to the old strict scaffolding behavior.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `docs/workflow/T-085/README.md`
- `docs/workflow/T-085/pr/diffstat.txt`
- `docs/workflow/T-085/pr/meta.json`
- `docs/workflow/T-085/pr/review.md`
- `docs/workflow/T-085/pr/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->
