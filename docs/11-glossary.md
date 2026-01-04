# Glossary

## Agent
A role with a JSON-defined scope and workflow.

## Task ID
A unique identifier like `202601031816-7F3K2Q` used to track work across backends.

## Workflow Artifact
Per-task documentation under [`.codex-swarm/tasks/<task-id>/`](../.codex-swarm/tasks/).

## PR Artifact
Local PR simulation files under [`.codex-swarm/tasks/<task-id>/pr/`](../.codex-swarm/tasks/).

## Worktree
A separate checkout used for task branches in `branch_pr` mode.

## workflow_mode
Config switch that chooses between `direct` and `branch_pr` workflows.

## Verify
Running declared checks for a task via `agentctl`.

## Guard
Pre-commit checks that validate staged files and commit messages.

## Backend
Pluggable task store that defines the canonical source of truth (local or redmine).

## Local Cache
The [`.codex-swarm/tasks/`](../.codex-swarm/tasks/) folder when backend=redmine; used for offline work and sync.
