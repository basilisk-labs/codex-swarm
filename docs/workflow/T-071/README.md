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

## Task Notes (legacy)

## Goal

- Ensure every task in `tasks.json` declares dependencies explicitly via `depends_on` (use an empty list `[]` when there are no dependencies), so the pipeline can reason about readiness and ordering consistently.

## Scope

- Update pipeline instructions:
  - `AGENTS.md`: make `depends_on` an explicit, always-present list in the task schema and add a rule that PLANNER must set it on task creation.
  - `.codex-swarm/agents/PLANNER.json`: require setting `depends_on` for every new task (and revisiting it when scope changes).

## Verification

- `python scripts/agentctl.py agents`
- `python scripts/agentctl.py task lint`
