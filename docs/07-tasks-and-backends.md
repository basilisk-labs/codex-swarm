# Tasks and Backends

## Summary
Tasks are routed through `agentctl`, which uses the active backend plugin to decide the source of truth. When `backend=local`, the canonical store is [`.codex-swarm/tasks/`](../.codex-swarm/tasks/). When `backend=redmine`, Redmine is canonical and the local folder acts as a cache/offline layer.

## Task Identity
- Canonical task ID format: `YYYYMMDDHHMM-<RAND>`
- Example: `202601031816-7F3K2Q`
- IDs are immutable once created.
- `agentctl` generates IDs via `task new` and checks for collisions.
- Redmine requires a valid `task_id` custom field for every issue; missing/invalid values are auto-filled on read.

## Local Storage Layout
Each task lives in a dedicated folder (see [`.codex-swarm/tasks/`](../.codex-swarm/tasks/)):
```
.codex-swarm/tasks/<task-id>/README.md
```
Use [`.codex-swarm/tasks/<task-id>/README.md`](../.codex-swarm/tasks/) as the canonical file path when linking from docs.

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
doc_version: 2
doc_updated_at: "2026-01-03T18:16:00Z"
doc_updated_by: "agentctl"
created_at: "2026-01-03T18:16:00Z"
---
```

## Task Doc Metadata
The per-task README includes structured sections (`Summary`, `Context`, `Scope`, `Risks`, `Verify Steps`, `Rollback Plan`, `Notes`).
- When backend=local, these sections are stored in the README body and exported as `doc`.
- When backend=redmine, the same `doc` payload is stored in a Redmine custom field, along with `doc_version`, `doc_updated_at`, and `doc_updated_by`.
- Use `python .codex-swarm/agentctl.py task doc show|set` to read/update the `doc` metadata without editing files directly.

## Backend Model
### local
- Canonical source: [`.codex-swarm/tasks/`](../.codex-swarm/tasks/).
- `agentctl` reads/writes frontmatter directly.
- `tasks.json` is generated from local tasks for browsing and integrations.

### redmine
- Canonical source: Redmine issues with a `task_id` custom field.
- The local task ID maps to the Redmine `task_id` custom field; the Redmine issue id is stored separately as `redmine_id`.
- Local tasks are a cache/offline layer (optional).
- `agentctl` auto-falls back to local when Redmine is unavailable (only when cache is enabled).
- When connectivity returns, `agentctl sync redmine` reconciles changes.
- Set `cache_dir` to an empty value to disable local cache completely (sync and offline fallback are unavailable).
- Comments and task doc metadata can be stored in Redmine custom fields (`comments`, `doc_version`, `doc_updated_at`, `doc_updated_by`) to keep parity with local.

## Offline Fallback and Conflicts
- Auto fallback happens whenever Redmine is unreachable.
- Offline writes are tracked as `dirty` until synced.
- On sync conflicts, `agentctl` shows a diff and requires an explicit decision:
  - `--conflict=prefer-local`
  - `--conflict=prefer-remote`
  - `--conflict=fail`

## Backend Plugins
Backends are packaged as shareable plugin folders (see [`.codex-swarm/backends/`](../.codex-swarm/backends/)):
```
.codex-swarm/backends/<backend-id>/
  backend.json
  backend.py
```
When linking a backend path, point to [`.codex-swarm/backends/`](../.codex-swarm/backends/).

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
    "custom_fields": {
      "task_id": 12,
      "verify": 13,
      "commit": 14,
      "doc": 15,
      "comments": 16,
      "doc_version": 17,
      "doc_updated_at": 18,
      "doc_updated_by": 19
    },
    "cache_dir": ".codex-swarm/tasks"
  }
}
```

The active backend is selected in [`.codex-swarm/config.json`](../.codex-swarm/config.json):
```json
"tasks_backend": {
  "config_path": ".codex-swarm/backends/redmine/backend.json"
}
```

## Exported JSON Snapshot
[`tasks.json`](../.codex-swarm/tasks.json) is generated from the canonical backend:
```bash
python .codex-swarm/agentctl.py task export --format json --out .codex-swarm/tasks.json
```

[`.codex-swarm/viewer/tasks.html`](../.codex-swarm/viewer/tasks.html) reads the exported view only.

## Core Commands
```bash
python .codex-swarm/agentctl.py task list
python .codex-swarm/agentctl.py task show 202601031816-7F3K2Q
python .codex-swarm/agentctl.py task add 202601031816-7F3K2Q --title "..." --description "..."
python .codex-swarm/agentctl.py task update 202601031816-7F3K2Q --description "..."
python .codex-swarm/agentctl.py task lint
# or run read-only commands with --lint to force validation

Global flags:
- `--quiet`: suppress non-essential output.
- `--verbose`: enable extra logging (when available).
- `--json`: emit JSON-formatted errors (for CI/integrations).
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
