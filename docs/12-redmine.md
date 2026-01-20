# Redmine Backend

## Summary
Redmine is a canonical backend option for tasks. When enabled, Redmine issues store the task source of truth, while [`.codex-swarm/tasks/`](../.codex-swarm/tasks/) acts as an offline cache layer.

## Enable or Disable via Recipe
Redmine support is delivered as a recipe so it can be enabled or disabled on demand.

Enable (recipe scenario):
- Run the `redmine-backend` recipe mini-CLI (for example, `install` or `enable`).
- It writes `.codex-swarm/backends/redmine/backend.json` and updates `.codex-swarm/config.json` with `tasks_backend.config_path`.
- It may run a connectivity check (for example, `verify-connection`) before activation.

Disable (recipe scenario):
- Run the `redmine-backend` recipe mini-CLI `disable` scenario.
- It resets `tasks_backend.config_path` to `.codex-swarm/backends/local/backend.json`.
- Local task data stays intact in [`.codex-swarm/tasks/`](../.codex-swarm/tasks/).

## Canonical Mapping
- Task IDs map to the `task_id` custom field in Redmine.
- Redmine issue IDs are not stored locally; issues are resolved via the `task_id` custom field.
- When Redmine is unreachable, `agentctl` falls back to the local cache (if enabled).
- Use `python .codex-swarm/agentctl.py sync redmine` to reconcile changes after connectivity returns.

## Routing Flow
1) Agents call `agentctl` for task operations (`task add`, `task update`, `task doc set`, `sync redmine`).
2) `agentctl` loads the active backend from `.codex-swarm/config.json`.
3) The Redmine backend writes to Redmine and updates the local cache under [`.codex-swarm/tasks/`](../.codex-swarm/tasks/).
4) The local backend remains the base store and offline cache regardless of remote activation.

## Custom Fields
Configure these custom fields in Redmine and map their IDs in `backend.json`:

- `task_id`: task identifier in `YYYYMMDDHHMM-<RAND>` format.
- `verify`: JSON list of verify commands (stored as JSON string).
- `commit`: JSON object `{ hash, message }` for closure tracking (stored as JSON string).
- `doc`: markdown body containing the task doc sections.
- `comments`: JSON list of `{ author, body }` comment entries.
- `doc_version`: integer doc schema version (currently `2`).
- `doc_updated_at`: ISO-8601 timestamp when doc was last updated by `agentctl`.
- `doc_updated_by`: source marker for doc updates (defaults to `agentctl`).

## Notes (Journals)
When the `comments` list grows, `agentctl` appends new entries to the issue journals as notes using the format:
`[comment] <author>: <body>`.

## Config Example
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
      "task_id": 1,
      "verify": 2,
      "commit": 3,
      "doc": 4,
      "comments": 5,
      "doc_version": 6,
      "doc_updated_at": 7,
      "doc_updated_by": 8
    },
    "cache_dir": ".codex-swarm/tasks"
  }
}
```

## Troubleshooting
- If Redmine is unreachable, allow offline fallback and sync later.
- If custom fields are missing or misconfigured, task updates will fail or lose metadata.
