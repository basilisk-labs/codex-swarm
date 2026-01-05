---
id: "202601041544-253P5B"
title: "Auto-generate task IDs + load .env for Redmine"
status: "TODO"
priority: "Нормальный"
owner: "Via Mentis Assistant"
depends_on: []
tags: ["agentctl", "redmine", "tasks", "docs", "env"]
verify: null
commit: null
comments: []
description: "Add agentctl auto-ID creation, load repo .env before backend initialization, and document task_id vs redmine_id."
dirty: false
id_source: "custom"
redmine_id: 392
---
# Summary

Enable agentctl to honor repo `.env` values for Redmine configuration and document the ID generation flow and task_id mapping.

# Scope

- Load `.env` in `agentctl` before backend initialization.
- Add `task new` auto-ID flow and document it for agents.
- Clarify Redmine `task_id` custom field mapping vs `redmine_id`.

# Risks

- Low risk: task creation and backend initialization change.

# Verify Steps

- `python3 .codex-swarm/agentctl.py task list --quiet`

# Rollback Plan

- Revert the agentctl and documentation changes.
