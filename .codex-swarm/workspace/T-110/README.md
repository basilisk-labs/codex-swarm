# T-110: agentctl: backend plugin loader + config support

## Summary

- Add backend plugin config loading (backend.json) and dynamic class loading.
- Keep behavior unchanged when no backend config is set.

## Goal

- Establish the backend plugin entrypoint so later tasks can route task operations through a selectable backend without changing the CLI surface.

## Scope

- Read optional `tasks_backend.config_path` from `.codex-swarm/config.json`.
- Validate backend config fields and resolve module path safely under the repo.
- Load backend class dynamically for later use.

## Risks

- Misconfigured backend configs could fail fast at startup; mitigated by clear error messages.
- Dynamic imports may mask path issues if not validated; mitigated by repo-root checks.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task list`

## Rollback Plan

- Revert `.codex-swarm/agentctl.py` changes and remove backend config references.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: add backend config resolution and dynamic class loader helpers.
<!-- END AUTO SUMMARY -->
