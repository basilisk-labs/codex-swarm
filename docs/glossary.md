# Glossary

## Agent
A role with a JSON-defined scope and workflow.

## Task ID
A unique identifier like T-123 used to track work in [`.codex-swarm/tasks.json`](../.codex-swarm/tasks.json).

## Workflow Artifact
Per-task documentation under [`.codex-swarm/workspace/T-123/`](../.codex-swarm/workspace/T-123/).

## PR Artifact
Local PR simulation files under [`.codex-swarm/workspace/T-123/pr/`](../.codex-swarm/workspace/T-123/pr/).

## Worktree
A separate checkout used for task branches in `branch_pr` mode.

## workflow_mode
Config switch that chooses between `direct` and `branch_pr` workflows.

## Verify
Running declared checks for a task via `agentctl`.

## Guard
Pre-commit checks that validate staged files and commit messages.
