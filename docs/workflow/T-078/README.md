# T-078: agentctl: pr check validates README completeness

## Summary

- Make `agentctl pr check` error messages point directly at `docs/workflow/T-###/README.md` when required sections are missing/empty.

## Goal

- Reduce time wasted hunting for the “PR doc” file by giving a concrete file path in validation failures.

## Scope

- `scripts/agentctl.py`: improve `pr check` messaging for missing/empty required sections in the PR doc.

## Risks

- Minimal behavior change; only affects error message text.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke:
  - Create a placeholder README for a task and run `python scripts/agentctl.py pr check T-###` to see the file path in the error.

## Rollback Plan

- Revert this task commit(s).

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
