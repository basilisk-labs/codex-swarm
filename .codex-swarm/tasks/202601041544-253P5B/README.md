---
id: "202601041544-253P5B"
title: "Auto-generate task IDs + load .env for Redmine"
status: "DONE"
priority: "Нормальный"
owner: "Via Mentis Assistant"
depends_on: []
tags: []
verify: null
commit: { hash: "decbfa9574e7df7e160329e92a7882763ba6ce16", message: "✨ 253P5B ensure task_id on create" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Redmine API check for custom_fields; no automated tests were run." }
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
