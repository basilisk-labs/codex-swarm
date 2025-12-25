# Tasks and Agentctl

## Canonical Task Source
- `.codex-swarm/tasks.json` is the single source of truth.
- Manual edits are not allowed because of checksum enforcement.

## Task Lifecycle
- Statuses: TODO, DOING, DONE, BLOCKED.
- Transitions are recorded via agentctl commands (`start`, `block`, `finish`).

## Core Commands
```bash
python .codex-swarm/agentctl.py task list
python .codex-swarm/agentctl.py task show T-123
python .codex-swarm/agentctl.py task add T-123 --title "..." --description "..." --depends-on "[]"
python .codex-swarm/agentctl.py task update T-123 --description "..."
python .codex-swarm/agentctl.py task lint
```

## Verification and Closure
```bash
python .codex-swarm/agentctl.py verify T-123
python .codex-swarm/agentctl.py finish T-123 --commit <git-rev> --author INTEGRATOR --body "Verified: ..."
```

## Guardrails
- Use `agentctl guard commit` before committing.
- Keep allowlists tight and scoped to the task.
