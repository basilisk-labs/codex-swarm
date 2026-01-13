---
id: "202601131643-6Z977J"
title: "Auto-create tasks after plan approval"
status: "DONE"
priority: "Нормальный"
owner: "REDMINE"
depends_on: []
tags: []
verify: null
commit: { hash: "e701172accefdfc0e34992471983363a9303ae33", message: "✨ 6Z977J auto-create tasks after plan approval: remove post-approval task prompt; update orchestrator guidance; sync agentctl doc" }
comments:
  - { author: "REDMINE", body: "Verified: documentation-only updates; no tests run; confirmed auto-task creation guidance." }
doc_version: 2
doc_updated_at: "2026-01-13T17:29:41+00:00"
doc_updated_by: "agentctl"
description: "Update orchestrator guidance so it auto-creates the top-level tracking task after plan approval unless the user explicitly opts out; remove the post-approval prompt asking whether to create tasks. Align AGENTS.md, .codex-swarm/agents/ORCHESTRATOR.json, and .codex-swarm/agentctl.md with the new flow."
dirty: false
id_source: "custom"
---
## Summary

Auto-create the top-level task after plan approval and remove the post-approval task prompt.

## Scope

AGENTS.md; .codex-swarm/agents/ORCHESTRATOR.json; .codex-swarm/agentctl.md.

## Risks

Low: documentation/instruction changes only; risk is confusing guidance if misread.

## Verify Steps

None (doc-only change).

## Rollback Plan

Revert commit e701172accef.

## Notes

Task creation is automatic after plan approval unless the user opts out.

