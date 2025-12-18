# T-087: Pin current git branch as base branch

## Summary

- When starting Codex Swarm in an existing git repo, automatically pin the current branch into `.codex-swarm/swarm.config.json` as `base_branch` (when missing) and use it as the default base for creating task branches/worktrees and for integration.

## Goal

- Ensure the workflow is branch-agnostic: if initialization happens on a non-`main` branch, that branch becomes the “mainline” for the run and `main` is not touched.

## Scope

- `.codex-swarm/swarm.config.json`: add optional `base_branch`.
- `scripts/agentctl.py`: replace hard-coded `main` defaults/guardrails with “base branch” derived from config (auto-pinned on first use).
- `AGENTS.md` and `.codex-swarm/agents/*.json`: update wording and commands to refer to the base branch (not `main`) where appropriate.

## Risks

- Medium: changes affect defaults for branch/worktree/integrate guardrails; incorrect base resolution could block workflow commands.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke:
  - Create and checkout a non-`main` branch (e.g. `git switch -c tmp/base-smoke`).
  - Remove `base_branch` from `.codex-swarm/swarm.config.json` (if present).
  - Run `python scripts/agentctl.py work start T-087 --agent CODER --slug smoke --worktree` and confirm config is updated with `"base_branch": "tmp/base-smoke"`.
  - Confirm `python scripts/agentctl.py integrate ...` runs only from the pinned base branch and targets it (not `main`).

## Rollback Plan

- Revert the changes; defaults and guardrails return to `main`-centric behavior.

