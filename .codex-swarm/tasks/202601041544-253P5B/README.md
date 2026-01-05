---
id: "202601041544-253P5B"
title: "Load .env for Redmine settings"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["agentctl", "redmine", "env"]
description: "Ensure agentctl loads the repo .env before backend initialization so Redmine env config is honored."
dirty: false
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
