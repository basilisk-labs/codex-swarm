---
id: "202601041253-0003K"
title: "agentctl: migrate tasks.json to local backend"
status: "DONE"
priority: "normal"
owner: "automation"
depends_on: []
tags: []
verify: null
commit: "3d8cd6dd2137ee90f303f6ca13d2f0f13cd412a6"
comments: []
description: "Add a migration/export command to seed .codex-swarm/tasks from tasks.json and set tasks_backend.config_path to the local backend."
dirty: false
id_source: "custom"
redmine_id: 269
---
# 202601041253-0003K: agentctl: migrate tasks.json to local backend

## Summary

- Add a migration command to seed `.codex-swarm/tasks/` from `.codex-swarm/tasks.json`.
- Point `tasks_backend.config_path` to the local backend plugin.

## Goal

- Make local backend the default canonical store while keeping a one-time migration path from tasks.json.

## Scope

- Add `agentctl task migrate` (reads tasks.json, writes via configured backend).
- Update `.codex-swarm/config.json` to use `.codex-swarm/backends/local/backend.json`.

## Risks

- Migration may overwrite tasks if run repeatedly without checks.
- Tasks with unexpected schemas may fail to serialize into frontmatter.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task migrate`
- `python3 .codex-swarm/agentctl.py task list`
- `python3 .codex-swarm/agentctl.py task export --out .codex-swarm/tasks.json`

## Rollback Plan

- Revert `.codex-swarm/config.json` and remove the migrate command.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: add `task migrate` command for seeding backend from tasks.json.
- `.codex-swarm/config.json`: set `tasks_backend.config_path` to local backend plugin.
<!-- END AUTO SUMMARY -->