# Troubleshooting

## tasks.json mismatch or stale data
- Cause: `tasks.json` is an exported view and may be stale.
- Fix: re-run `python .codex-swarm/agentctl.py task export --format json --out .codex-swarm/tasks.json`.

## Dirty working tree before commit
- Cause: unrelated edits or forgotten files.
- Fix: `git status --short`, then stash or commit only what belongs to the task.

## Outdated task state
- Cause: viewing stale data from cache or a previous export.
- Fix: re-run `python .codex-swarm/agentctl.py task list` or `task show`, then sync if needed.

## Redmine unreachable
- Cause: network outage or API credentials expired.
- Fix: allow the auto offline fallback, then run `python .codex-swarm/agentctl.py sync redmine` once connectivity returns.

## Redmine sync conflicts
- Cause: local cache diverged from Redmine.
- Fix: re-run sync and choose a conflict strategy (`--conflict=prefer-local|prefer-remote|fail`) after reviewing the diff.

## agentctl command failures
- Cause: running from the wrong directory or missing Python.
- Fix: run from the repo root and ensure Python 3.10+ is available.

## IDE or plugin stops responding
- Fix: restart the IDE or reload the project, then re-run the last command manually.
