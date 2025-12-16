# agentctl quickstart

`python scripts/agentctl.py` is the only supported way to inspect/update `tasks.json` (manual edits break the checksum).

## Common commands

```bash
# list/show
python scripts/agentctl.py task list
python scripts/agentctl.py task show T-123

# validate tasks.json (schema/deps/checksum)
python scripts/agentctl.py task lint

# readiness gate (deps DONE)
python scripts/agentctl.py ready T-123

# status transitions that require structured comments
python scripts/agentctl.py start T-123 --author CODER --body "Start: ... (why, scope, plan, risks)"
python scripts/agentctl.py block T-123 --author CODER --body "Blocked: ... (what blocks, next step, owner)"

# run per-task verify commands (declared on the task)
python scripts/agentctl.py verify T-123

# before committing, validate staged allowlist + message quality
python scripts/agentctl.py guard commit T-123 -m "✨ T-123 Short meaningful summary" --allow <path-prefix>

# if you want a safe wrapper that also runs `git commit`
python scripts/agentctl.py commit T-123 -m "✨ T-123 Short meaningful summary" --allow <path-prefix>

# when closing a task: mark DONE + attach commit metadata (typically after implementation commit)
python scripts/agentctl.py finish T-123 --commit <git-rev> --author REVIEWER --body "Verified: ... (what ran, results, caveats)"
```

## Ergonomics helpers

```bash
# find tasks that are ready to start (deps DONE)
python scripts/agentctl.py task next

# search tasks by text (title/description/tags/comments)
python scripts/agentctl.py task search agentctl

# scaffold a workflow artifact (docs/workflow/T-###.md)
python scripts/agentctl.py task scaffold T-123

# suggest minimal --allow prefixes based on staged files
python scripts/agentctl.py guard suggest-allow
python scripts/agentctl.py guard suggest-allow --format args
```

## Workflow reminders

- `tasks.json` is canonical; do not edit it by hand.
- Keep work atomic: one task → one implementation commit (plus planning + closure commits if you use the 3-phase cadence).
- Prefer `start/block/finish` over `task set-status`.
- Keep allowlists tight: pass only the path prefixes you intend to commit.
