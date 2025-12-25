# Workflow

## End-to-End Flow
1. You state a goal to the ORCHESTRATOR.
2. ORCHESTRATOR proposes a plan and asks for approval.
3. PLANNER creates or updates tasks in `.codex-swarm/tasks.json` using `agentctl`.
4. Execution agents implement changes and update workflow artifacts.
5. REVIEWER assesses changes and leaves handoff notes.
6. INTEGRATOR verifies, merges, and closes tasks (when `workflow_mode=branch_pr`).

## Planning and Tasks
- Every task is atomic and tracked by ID (T-###).
- `.codex-swarm/tasks.json` is canonical and checksum-protected.
- Task changes are done only via `python .codex-swarm/agentctl.py`.

## Implementation
- CODER implements changes with tight diffs and clear validation notes.
- TESTER adds or updates tests when behavior changes.
- DOCS updates user-facing docs and task artifacts.

## Verification and Closure
- Use `python .codex-swarm/agentctl.py verify T-123` to run declared checks.
- Closure updates `.codex-swarm/tasks.json` via `finish`.
- A clean git status is required before handoff.

## Commit Expectations
- One task maps to one implementation commit.
- Planning and closure commits are used when required by the workflow.
- Commit messages are short, emoji-prefixed, and include the task ID.
