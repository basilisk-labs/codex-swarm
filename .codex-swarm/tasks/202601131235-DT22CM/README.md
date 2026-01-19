---
id: "202601131235-DT22CM"
title: "Map agentctl commands by agent and phase"
status: "DONE"
priority: "normal"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["agentctl", "agents"]
commit: { hash: "bc30c58e49fae183e38567424944e97a2e8fe2ab", message: "✨ DT22CM map agentctl commands by role and phase" }
comments:
  - { author: "ORCHESTRATOR", body: "Verified: Docs-only change; updated agentctl role/phase mapping and task artifact; no runtime impact." }
doc_version: 2
doc_updated_at: "2026-01-13T12:42:00+00:00"
doc_updated_by: "agentctl"
description: "Analyze agentctl docs and agent specs to map which agent can use which agentctl commands at each workflow stage, then update agentctl.md so agents can avoid extra help calls."
---
## Summary

Added a role/phase command guide to agentctl.md so agents can map commands to workflow moments.

## Context

Request was to map agentctl commands to agents and workflow phases based on agent specs and CLI docs.

## Scope

Updated only .codex-swarm/agentctl.md; no CLI behavior changes.

## Risks

Low; docs could drift if commands change.

## Verify Steps

None (docs-only).

## Rollback Plan

Revert the doc change and task artifacts.

## Notes

Commands listed align with .codex-swarm/agents/*.json and current agentctl.md examples.

