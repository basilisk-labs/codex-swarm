# Troubleshooting

## tasks.json checksum errors
- Cause: manual edits to `.codex-swarm/tasks.json`.
- Fix: revert the manual change and reapply via `agentctl`.

## Dirty working tree before commit
- Cause: unrelated edits or forgotten files.
- Fix: `git status --short`, then stash or commit only what belongs to the task.

## Outdated task state
- Cause: viewing stale task data.
- Fix: re-run `python .codex-swarm/agentctl.py task list` or `task show`.

## agentctl command failures
- Cause: running from the wrong directory or missing Python.
- Fix: run from the repo root and ensure Python 3.10+ is available.

## IDE or plugin stops responding
- Fix: restart the IDE or reload the project, then re-run the last command manually.
