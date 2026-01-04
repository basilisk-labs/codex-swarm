# Branching and PR Artifacts

## workflow_mode
Configured in [`.codex-swarm/config.json`](../.codex-swarm/config.json).

### direct
- Single-checkout workflow.
- Task branches and PR artifacts are optional.
- Tasks can be implemented and closed on the current branch.

### branch_pr
- Task branches and worktrees are required.
- Canonical task writes happen only on the base branch.
- INTEGRATOR performs verify, merge, and finish.

## Task Branches and Worktrees
- Branch naming: `task/<task-id>/<slug>`.
- Worktrees live under [`.codex-swarm/worktrees/`](../.codex-swarm/worktrees/).

## PR Artifacts
- Location: [`.codex-swarm/tasks/<task-id>/pr/`](../.codex-swarm/tasks/).
- Files: `meta.json`, `diffstat.txt`, `verify.log`, `review.md`.
- Purpose: local PR simulation for review and integration.

## Handoff Notes
- Reviewers and executors record handoff notes in `review.md`.
- INTEGRATOR appends notes into the task closure record.

## Planned Expansions
- Document how PR artifacts behave when backend=redmine (cache vs canonical).
