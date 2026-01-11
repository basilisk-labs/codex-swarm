---
id: "202601111125-KZKBQ7"
title: "Normalize Redmine owners to agent"
status: "TODO"
priority: "low"
owner: "CODER"
depends_on: []
tags: ["redmine", "ownership"]
doc_version: 2
doc_updated_at: "2026-01-11T11:40:17+00:00"
doc_updated_by: "agentctl"
description: "Ensure Redmine-backed tasks use a configured agent owner (REDMINE) and retag existing tasks."
---
## Summary

Ensure Redmine tasks map owner to configured agent (default REDMINE) and clean existing tasks.

## Context

- Some tasks imported from Redmine were assigned to the assignee name (Via Mentis Assistant) instead of an agent id.
- We want owner fields to always be agent ids; the Redmine executor is effectively the API key owner.

## Scope

- Add owner_agent setting to Redmine backend (env override allowed) and default to REDMINE.
- Map owner from Redmine issues to the configured agent when listing.
- Update existing local task READMEs that used the assignee name to use REDMINE.

## Risks

- Changing owner mapping could surprise consumers expecting assignee names.
- Legacy exports may still contain old owners until refreshed.

## Verify Steps

- python -m py_compile .codex-swarm/backends/redmine/backend.py
- python .codex-swarm/agentctl.py task list --owner REDMINE

## Rollback Plan

- Revert .codex-swarm/backends/redmine/backend.py and the adjusted task READMEs.

