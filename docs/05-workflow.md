# Workflow

## End-to-End Flow
1. You state a goal to the ORCHESTRATOR.
2. ORCHESTRATOR proposes a plan and asks for approval.
3. PLANNER creates or updates tasks via `agentctl` against the active backend.
4. Execution agents implement changes and update workflow artifacts.
5. REVIEWER assesses changes and leaves handoff notes.
6. INTEGRATOR verifies, merges, and closes tasks (when `workflow_mode=branch_pr`).

## Planning and Tasks
- Every task is atomic and tracked by ID (`YYYYMMDDHHMM-<RAND>`).
- The canonical task source depends on the backend:
  - `local`: [`.codex-swarm/tasks/`](../.codex-swarm/tasks/) is canonical.
  - `redmine`: Redmine is canonical; [`.codex-swarm/tasks/`](../.codex-swarm/tasks/) is a cache/offline layer.
- Task changes are done only via `python .codex-swarm/agentctl.py`.

## Implementation
- CODER implements changes with tight diffs and clear validation notes.
- TESTER adds or updates tests when behavior changes.
- DOCS updates user-facing docs and task artifacts.
- Before handoff, update the task doc metadata (Summary/Scope/Risks/Verify Steps/Rollback Plan).
- Each agent leaving a task must leave a handoff comment:
  - `workflow_mode=branch_pr`: add notes under `## Handoff Notes` in `.codex-swarm/tasks/<task-id>/pr/review.md`.
  - `workflow_mode=direct`: use `python .codex-swarm/agentctl.py task comment <task-id> --author <ROLE> --body "..."`

## Templates and Checklists

### Task README Template (required sections)
Use `python .codex-swarm/agentctl.py task doc set <task-id> --section <Section> --text "..."` for each section.

```text
Summary: One sentence on what changed and why.
Context: Key constraints, links, or assumptions.
Scope:
- In scope: ...
- Out of scope: ...
Risks: What could break and how you mitigated it.
Verify Steps: Exact commands run (or "Not run (docs-only).").
Rollback Plan: How to revert safely.
Notes: Optional follow-ups or handoff details.
```

### Status Comment Templates
Check the required prefixes/min lengths via `python .codex-swarm/agentctl.py config show`.

```text
Start: Short plan + scope + any blockers (40+ chars).
Blocked: What blocks you, owner, and next step (40+ chars).
Verified: What you ran, results, and caveats (60+ chars).
```

### Direct Mode Checklist (workflow_mode=direct)
- Confirm mode: `python .codex-swarm/agentctl.py config show`.
- Update task docs: Summary/Scope/Risks/Verify Steps/Rollback Plan.
- Guardrails: `guard clean` -> `guard scope` -> stage allowed paths -> `agentctl commit`.
- Verify: `python .codex-swarm/agentctl.py verify <task-id>` (if declared).
- Finish: `python .codex-swarm/agentctl.py finish <task-id> --commit <rev> --author <OWNER> --body "Verified: ..."`.

### Branch PR Checklist (workflow_mode=branch_pr)
- Start worktree: `python .codex-swarm/agentctl.py work start <task-id> --agent <ROLE> --slug <slug> --worktree`.
- Open/update PR artifacts: `python .codex-swarm/agentctl.py pr open ...` then `python .codex-swarm/agentctl.py pr update <task-id>` after changes.
- Commit on task branch only; never stage `.codex-swarm/tasks.json` in a task branch.
- INTEGRATOR: `pr check` -> `integrate` -> `finish`.

## Verification and Closure
- Use `python .codex-swarm/agentctl.py verify 202601031816-7F3K2Q` to run declared checks.
- Closure updates the canonical backend via `finish`, then refreshes the local cache/export.
- A clean git status is required before handoff.

## Commit Expectations
- One task maps to one implementation commit.
- Planning and closure commits are used when required by the workflow.
- Commit messages are short, emoji-prefixed, and include the task ID.

## Planned Expansions
- Add a section on offline-first behavior when Redmine is unavailable.
- Add a quick example of task creation in `local` vs `redmine` backends.
