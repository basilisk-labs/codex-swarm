# Branching and PR Artifacts

## workflow_mode
Configured in `.codex-swarm/config.json`.

### direct
- Single-checkout workflow.
- Task branches and PR artifacts are optional.
- Tasks can be implemented and closed on the current branch.

### branch_pr
- Task branches and worktrees are required.
- `.codex-swarm/tasks.json` is updated only on the base branch.
- INTEGRATOR performs verify, merge, and finish.

## Task Branches and Worktrees
- Branch naming: `task/T-123/<slug>`.
- Worktrees live under `.codex-swarm/worktrees/`.

## PR Artifacts
- Location: `.codex-swarm/workspace/T-123/pr/`.
- Files: `meta.json`, `diffstat.txt`, `verify.log`, `review.md`.
- Purpose: local PR simulation for review and integration.

## Handoff Notes
- Reviewers and executors record handoff notes in `review.md`.
- INTEGRATOR appends notes into the task closure record.
