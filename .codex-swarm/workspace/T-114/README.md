# T-114: agentctl: migrate workspace paths to tasks/ + PR artifacts

## Summary

- Move workflow/PR artifact paths from `.codex-swarm/workspace/` to `.codex-swarm/tasks/`.
- Preserve legacy fallbacks for existing workspace-based artifacts.

## Goal

- Align agentctl path resolution and CLI help strings with the new local task storage location.

## Scope

- Update `.codex-swarm/config.json` workflow_dir to `.codex-swarm/tasks`.
- Update agentctl path helpers and messages to use tasks/.
- Add legacy fallbacks for existing workspace-based artifacts.

## Risks

- Legacy artifacts may not be discovered if fallback paths are incomplete.
- Existing scripts that hardcode workspace paths may need updates.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task scaffold <task-id> --force`
- `python3 .codex-swarm/agentctl.py pr open <task-id> --author CODER --branch task/<task-id>/slug`

## Rollback Plan

- Revert `.codex-swarm/agentctl.py` path changes and reset `workflow_dir` in config.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: swap workspace paths to tasks/ and add legacy fallbacks.
- `.codex-swarm/config.json`: point workflow_dir at `.codex-swarm/tasks`.
<!-- END AUTO SUMMARY -->
