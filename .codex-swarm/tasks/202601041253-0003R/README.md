---
id: "202601041253-0003R"
title: "Migrate legacy task IDs to new format"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "f84ae1546f3077d674c659dce3ce9bf690160894", message: "🆔 202601041253-0003R migrate legacy task IDs" }
comments:
  - { author: "INTEGRATOR", body: "Verified: python3 .codex-swarm/agentctl.py task list --quiet; ids migrated." }
description: "Re-ID existing tasks to the new timestamp + short ID format while preserving order and dependencies."
dirty: false
redmine_id: 279
---
# 202601041253-0003R: Migrate legacy task IDs to new format

## Summary

- Added `task reid` to migrate legacy `T-###` folders into the new timestamp+suffix ID format.
- Updated docs and prompts to use `<task-id>` placeholders instead of legacy numbering.
- Rewrote task folders/IDs and exported the updated `.codex-swarm/tasks.json` snapshot.

## Goal

- Transition the repository to the new task ID scheme while keeping dependencies and ordering intact.

## Scope

- `.codex-swarm/agentctl.py`: implement `task reid` for the local backend and update user-facing examples.
- `.codex-swarm/tasks/`: rename task directories, update frontmatter and headings.
- `.codex-swarm/tasks.json`: export the new snapshot after migration.

## Risks

- Task IDs change permanently; external references to legacy `T-###` IDs will be stale.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task list --quiet`
- `python3 .codex-swarm/agentctl.py task show 202601041253-0003R`

## Rollback Plan

- Restore `.codex-swarm/tasks/` and `.codex-swarm/tasks.json` from git history.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: add task re-id command and update help text examples.
- `.codex-swarm/tasks/`: rename legacy task folders to new IDs and refresh frontmatter headings.
- `.codex-swarm/tasks.json`: export snapshot after re-identification.
- `AGENTS.md`: replace legacy task id examples with `<task-id>` placeholders.
- `.codex-swarm/agentctl.md`: update quickstart examples for new task ids.
- `.codex-swarm/agents/*.json`: swap legacy task id paths to `<task-id>` placeholders.
<!-- END AUTO SUMMARY -->
