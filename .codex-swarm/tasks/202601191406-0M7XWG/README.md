---
id: "202601191406-0M7XWG"
title: "Refresh tasks viewer"
status: "DONE"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
commit: { hash: "b9555c09a8e4e4da350a2a5752e7ca30e92abee2", message: "✨ 0M7XWG refresh tasks viewer" }
doc_version: 2
doc_updated_at: "2026-01-19T14:07:09+00:00"
doc_updated_by: "agentctl"
description: "Capture the recent viewer redesign as a tracked task so the changes are documented and committed cleanly."
---
## Summary

Document the viewer redesign so it is tracked and committed as a standalone task.

## Scope

- Package the existing changes in the tasks viewer UI and server endpoint into this task.
- Keep the scope limited to the viewer refresh already implemented in `.codex-swarm/viewer/`.

## Risks

Risk: the refreshed UI could introduce regressions in filtering or status updates, so we should spot-check the main flows.

## Verify Steps

- Run the viewer locally and ensure the tabs, task list, and status updates render.

## Rollback Plan

Revert the viewer changes in `.codex-swarm/viewer/tasks.html` and `.codex-swarm/viewer/tasks_server.py` if issues arise.

## Notes

No additional dependencies or migrations.

