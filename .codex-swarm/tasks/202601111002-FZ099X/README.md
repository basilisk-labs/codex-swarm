---
id: "202601111002-FZ099X"
title: "Redmine backend CRUD check"
status: "TODO"
priority: "low"
owner: "CODER"
depends_on: []
tags: ["redmine"]
verify: []
comments:
  - { author: "CODER", body: "Test comment via Redmine backend" }
doc_version: 2
doc_updated_at: "2026-01-11T10:03:42+00:00"
doc_updated_by: "agentctl"
description: "Create/update/comment tasks directly against Redmine backend to verify CLI flows."
dirty: false
id_source: "custom"
redmine_id: 427
---
## Summary

Validate that Redmine backend supports create/update/comment flows via agentctl in sandbox.

## Context

- Need assurance that Redmine backend works end-to-end with the current CLI without backend-specific hacks.
- Sandbox project is cleared; repo state is canonical so new tasks should appear and round-trip cleanly.

## Scope

- Create the task via Redmine backend and confirm it appears in task list.
- Update doc sections and add a comment to verify custom fields and journals.
- Pull the task again to confirm fields persist.

## Risks

- API latency could cause commands to time out; retries may be needed.
- If sandbox contains old data, lists may mix test and legacy issues.

## Verify Steps

- python .codex-swarm/agentctl.py task show 202601111002-FZ099X --quiet
- python .codex-swarm/agentctl.py task comment 202601111002-FZ099X --author CODER --body "Test comment via Redmine backend"
- python .codex-swarm/agentctl.py task doc show 202601111002-FZ099X --quiet

## Rollback Plan

- Delete the test issue from Redmine if it pollutes the sandbox.
- Re-run task list to confirm it is gone.
