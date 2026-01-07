# Redmine Backend

## Summary
Redmine is a canonical backend option for tasks. When enabled, Redmine issues store the task source of truth, while [`.codex-swarm/tasks/`](../.codex-swarm/tasks/) acts as an offline cache layer.

## Canonical Mapping
- Task IDs map to the `task_id` custom field in Redmine.
- Redmine issue IDs are stored in task payloads as `redmine_id`.
- When Redmine is unreachable, `agentctl` falls back to the local cache (if enabled).
- Use `python .codex-swarm/agentctl.py sync redmine` to reconcile changes after connectivity returns.

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

## Troubleshooting
- If Redmine is unreachable, allow offline fallback and sync later.
- If custom fields are missing or misconfigured, task updates will fail or lose metadata.
