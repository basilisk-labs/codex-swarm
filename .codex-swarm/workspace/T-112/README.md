# T-112: agentctl: route task commands to backend + new sync/export commands

## Summary

- Route task operations through a backend-aware task store with a safe fallback to `tasks.json` when no backend is configured.
- Add `task export` and `sync` CLI commands.

## Goal

- Keep the CLI interface stable while enabling backend routing for list/show/update/finish and new export/sync commands.

## Scope

- Add backend-aware task store helpers and update task commands to use them.
- Add `task export` for writing a JSON snapshot under repo root.
- Add `sync` command that delegates to backend implementations.

## Risks

- Backend-enabled runs could behave differently if the backend API is incomplete.
- Exported JSON may diverge from canonical state if tasks are updated outside agentctl.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task list`
- `python3 .codex-swarm/agentctl.py task export --out .codex-swarm/tasks.json`

## Rollback Plan

- Revert `.codex-swarm/agentctl.py` changes and remove new CLI commands.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: add backend-aware task store, export command, and sync CLI.
<!-- END AUTO SUMMARY -->
