# T-059: Add agentctl git/task ergonomics

## Goal

Reduce friction for common workflows (finding the next ready task, scaffolding workflow artifacts, and committing safely) by adding small, focused `agentctl` subcommands.

## Scope

- Add `task next` (list tasks ready to start).
- Add `task search` (text search across tasks fields).
- Add `task scaffold` (create `.codex-swarm/workspace/T-###/README.md` from a template).
- Add `guard suggest-allow` (suggest minimal `--allow` prefixes for staged files).
- Add `commit` wrapper (runs guard checks then executes `git commit`).

## Verification

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py guard --help`

## Implementation Notes

- Implemented new subcommands in `scripts/agentctl.py`:
  - `task next` filters tasks by readiness (deps DONE) plus optional status/owner/tag filters.
  - `task search` searches across common task text fields (supports `--regex`).
  - `task scaffold` writes `.codex-swarm/workspace/T-###/README.md` skeletons (uses existing task title by default).
  - `guard suggest-allow` derives minimal `--allow` prefixes from staged paths.
  - `commit` runs the same checks as `guard commit`, then calls `git commit` (optional `--auto-allow`).
- Updated `.codex-swarm/agentctl.md` to document the new helpers.
