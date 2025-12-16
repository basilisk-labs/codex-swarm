# T-072: agentctl task add: default depends_on to []

## Summary

- Ensure every newly created task includes an explicit `depends_on` list by default (`[]` when none), so dependency handling stays consistent and machine-checkable.

## Scope

- `scripts/agentctl.py`: `task add` always writes `depends_on` (empty list when no `--depends-on` flags are provided).
- `AGENTS.md`: clarify that the `depends_on` requirement applies to newly added tasks (legacy tasks may still omit it until updated).

## Risks

- Minimal: changes JSON shape for new tasks by adding an empty `depends_on` field.

## Verify Steps

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py agents`

## Rollback Plan

- Revert this task branch.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
