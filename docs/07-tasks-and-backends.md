# Tasks and Backends

## Summary
Tasks are routed through `agentctl`, which uses the active backend plugin to decide the source of truth. When `backend=local`, the canonical store is `.codex-swarm/tasks/`. When `backend=redmine`, Redmine is canonical and the local folder acts as a cache/offline layer.

## Task Identity
- Canonical task ID format: `YYYYMMDDHHMM-<RAND>`
- Example: `202601031816-7F3K2Q`
- IDs are immutable once created.
- `agentctl` checks for collisions when generating new IDs.

## Local Storage Layout
Each task lives in a dedicated folder:
```
.codex-swarm/tasks/<task-id>/README.md
```

The `README.md` begins with frontmatter:
```yaml
---
id: "202601031816-7F3K2Q"
title: "Add Normalizer Service"
status: "TODO"
priority: "med"
owner: "human"
depends_on: ["202601031700-9Q2X5M"]
tags: ["codextown", "normalizer"]
verify: ["python -m pytest -q"]
commit: { hash: "...", message: "..." }
comments:
  - { author: "owner", body: "Context..." }
created_at: "2026-01-03T18:16:00Z"
---
```

## Backend Model
### local
- Canonical source: `.codex-swarm/tasks/`.
- `agentctl` reads/writes frontmatter directly.
- `tasks.json` is generated from local tasks for browsing and integrations.

### redmine
- Canonical source: Redmine issues with a `task_id` custom field.
- Local tasks are a cache/offline layer.
- `agentctl` auto-falls back to local when Redmine is unavailable.
- When connectivity returns, `agentctl sync redmine` reconciles changes.

## Offline Fallback and Conflicts
- Auto fallback happens whenever Redmine is unreachable.
- Offline writes are tracked as `dirty` until synced.
- On sync conflicts, `agentctl` shows a diff and requires an explicit decision:
  - `--conflict=prefer-local`
  - `--conflict=prefer-remote`
  - `--conflict=fail`

## Backend Plugins
Backends are packaged as shareable plugin folders:
```
.codex-swarm/backends/<backend-id>/
  backend.json
  backend.py
```

`backend.json` points to the implementation and settings:
```json
{
  "id": "redmine",
  "version": 1,
  "module": "backend.py",
  "class": "RedmineBackend",
  "settings": {
    "url": "https://redmine.example.com",
    "api_key": "REDACTED",
    "project_id": "my-project",
    "status_map": { "TODO": 1, "DOING": 2, "BLOCKED": 3, "DONE": 4 },
    "custom_fields": { "task_id": 12, "verify": 13, "commit": 14 }
  }
}
```

The active backend is selected in `.codex-swarm/config.json`:
```json
"tasks_backend": {
  "config_path": ".codex-swarm/backends/redmine/backend.json"
}
```

## Exported JSON Snapshot
`tasks.json` is generated from the canonical backend:
```bash
python .codex-swarm/agentctl.py task export --format json --out .codex-swarm/tasks.json
```

`tasks.html` reads the exported snapshot only.

## Core Commands
```bash
python .codex-swarm/agentctl.py task list
python .codex-swarm/agentctl.py task show 202601031816-7F3K2Q
python .codex-swarm/agentctl.py task add 202601031816-7F3K2Q --title "..." --description "..."
python .codex-swarm/agentctl.py task update 202601031816-7F3K2Q --description "..."
python .codex-swarm/agentctl.py task lint
```

## Verification and Closure
```bash
python .codex-swarm/agentctl.py verify 202601031816-7F3K2Q
python .codex-swarm/agentctl.py finish 202601031816-7F3K2Q --commit <git-rev> --author INTEGRATOR --body "Verified: ..."
```

## Guardrails
- Use `agentctl guard commit` before committing.
- Keep allowlists tight and scoped to the task.
- Avoid editing frontmatter manually; use `agentctl`.

## Planned Expansions
- Document the `dirty` flag and cache reconciliation rules in detail.
- Add examples for Redmine field mappings and status transitions.
- Provide a template backend plugin for new integrations.
