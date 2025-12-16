# T-071: Require explicit depends_on on task add

## Summary

- Require explicit `depends_on` for every new task (use `[]` when none) so readiness and ordering stay machine-checkable.

## Scope

- `AGENTS.md`: clarify `depends_on` as required (always-present list) + add protocol note for task creation.
- `.codex-swarm/agents/PLANNER.json`: require PLANNER to set dependencies (or ask when unclear).

## Risks

- This is documentation-level enforcement; existing tasks may still omit `depends_on` until PLANNER updates them during normal edits.

## Verify Steps

- `python scripts/agentctl.py agents`
- `python scripts/agentctl.py task lint`

## Rollback Plan

- Revert this task branch.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
