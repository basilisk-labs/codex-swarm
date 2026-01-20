---
id: "202601041253-00002"
title: "Restructure agent registry into JSON files"
status: "DONE"
priority: "normal"
owner: "REDMINE"
depends_on: []
tags: ["agents"]
verify: null
commit: { hash: "31504cd01c8c3787e14531465e9f9c0278c1f78f", message: "✨ 00002 document agent registry JSON completion" }
comments:
  - { author: "REDMINE", body: "verified: not run (docs-only) | details: agent registry stored as JSON under .codex-swarm/agents and referenced by AGENTS.md." }
doc_version: 2
doc_updated_at: "2026-01-20T08:40:58+00:00"
doc_updated_by: "agentctl"
description: "Split every reusable agent prompt into a dedicated JSON file under .AGENTS for easier maintenance."
dirty: false
id_source: "custom"
---
## Summary

Agent registry now lives as individual JSON files under .codex-swarm/agents, with AGENTS.md as the shared source of truth.

## Scope

- Split agent prompts into JSON files in .codex-swarm/agents.\n- Keep AGENTS.md as the shared rule set referenced by each role.

## Risks

Low: structural/docs change only; risk limited to misaligned agent JSON content.

## Verify Steps

Not run (docs-only); confirmed .codex-swarm/agents/*.json exists for registered roles.

## Rollback Plan

Revert commits that introduced .codex-swarm/agents and restore the prior registry layout.

## Notes

Superseded by completed agent JSON registry work (e.g., 202601041253-0000A, 202601041253-0002T).

