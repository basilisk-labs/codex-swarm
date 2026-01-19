---
id: "202601191530-HJTDZK"
title: "Require tags on new tasks"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["agents", "tasks", "workflow"]
doc_version: 2
doc_updated_at: "2026-01-19T15:47:13+00:00"
doc_updated_by: "agentctl"
description: "Ensure task creation enforces non-empty tags and update agent guidance to always pass tags when creating tasks."
---
## Summary

Enforce non-empty tags when creating tasks and document the requirement for agents.

## Scope

Update agentctl task creation validation and adjust agentctl/AGENTS/agent guidance to mention required tags.

## Risks

Task creation without tags will now error, which may break existing automation. Document the requirement and keep the error message clear.

## Verify Steps

1) python .codex-swarm/agentctl.py task new --title 'Tmp' --description 'Tmp' --priority low --owner ORCHESTRATOR --depends-on '[]' --tag smoke. 2) python .codex-swarm/agentctl.py task new --title 'Tmp2' --description 'Tmp2' --priority low --owner ORCHESTRATOR --depends-on '[]' (expect error for missing tags).

## Rollback Plan

Revert the commit and rerun agentctl task lint if needed.

