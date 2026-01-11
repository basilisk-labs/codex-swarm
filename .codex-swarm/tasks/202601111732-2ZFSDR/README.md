---
id: "202601111732-2ZFSDR"
title: "Update GitHub sync scripts and cleanup"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["github", "sync", "cleanup", "scripting"]
verify: [".venv/bin/ruff format .", ".venv/bin/ruff check .", ".venv/bin/mypy"]
doc_version: 2
doc_updated_at: "2026-01-11T17:33:29+00:00"
doc_updated_by: "agentctl"
description: "Align GitHub task sync scripts with current backend/schema and keep viewer.sh during cleanup."
---
## Summary

Update GitHub task sync scripts/workflow to match current backend schema and keep viewer.sh during cleanup.

## Scope

- Align .github/scripts/sync_tasks.py with current tasks export fields and backend behavior.
- Adjust .github/workflows/sync-tasks.yml if needed for new args/envs.
- Remove viewer.sh from clean scripts so it is preserved.

## Risks

- GitHub API schema or project fields may differ from expected values.
- Workflow token permissions could block updates.

## Verify Steps

- .venv/bin/ruff format .
- .venv/bin/ruff check .
- .venv/bin/mypy

## Rollback Plan

- ...

