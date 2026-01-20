---
id: "202601130946-EPQFXS"
title: "Deduplicate agent JSON rules + batch ops guidance"
status: "DOING"
priority: "normal"
owner: "CODER"
depends_on: []
tags: ["agents", "docs", "agentctl"]
comments:
  - { author: "CODER", body: "Start: deduplicate shared guidance in agent JSON files and add batch task add/finish guidance in docs." }
doc_version: 2
doc_updated_at: "2026-01-20T08:47:55+00:00"
doc_updated_by: "agentctl"
description: "Trim shared guidance in .codex-swarm/agents/*.json to role-specific content and point to AGENTS.md and agentctl.md; update docs to encourage batch task add/finish to reduce backend writes."
---
## Summary

Agent JSON guidance is trimmed to role-specific content with shared rules in AGENTS.md/agentctl.md; batch ops guidance is documented.

## Context

Agent JSON files repeated common workflow rules; centralizing shared guidance in AGENTS.md and agentctl.md reduces prompt duplication. Batch task operations encourage write_tasks usage to reduce repeated writes.

## Scope

- Simplify .codex-swarm/agents/*.json to role-specific guidance with references to AGENTS.md and .codex-swarm/agentctl.md.
- Add batch task add/finish guidance in AGENTS.md and .codex-swarm/agentctl.md.

## Risks

Over-trimming could remove role-specific constraints; ensure shared rules remain in AGENTS.md and agentctl.md.

## Verify Steps

rg -n "Follow shared workflow rules" .codex-swarm/agents/*.json\nrg -n "batch" AGENTS.md .codex-swarm/agentctl.md

## Rollback Plan

Revert the AGENTS.md, .codex-swarm/agentctl.md, and .codex-swarm/agents/*.json changes.

## Notes

Superseded by agent/dedup cleanup tasks (202601131304-E1625C, 202601071301-JGRGE3) and agentctl docs updates.

