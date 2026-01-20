---
id: "202601200756-M04JPT"
title: "Align task-creation authority across ORCHESTRATOR/PLANNER"
status: "TODO"
priority: "med"
owner: "DOCS"
depends_on: ["[\"202601200756-3RRHDD\"]"]
tags: []
doc_version: 2
doc_updated_at: "2026-01-20T08:11:05+00:00"
doc_updated_by: "agentctl"
description: "Resolve conflicting guidance on who creates top-level tasks; update AGENTS.md and role JSONs to match a single rule."
---
## Summary

Align task-creation authority: ORCHESTRATOR creates the single top-level tracking task after plan approval; PLANNER creates downstream tasks.

## Scope

- Clarify ORCHESTRATOR vs PLANNER task-creation responsibilities in AGENTS.md.\n- Update ORCHESTRATOR.json and PLANNER.json to match the shared rule.

## Risks

Low: documentation-only alignment; no runtime behavior changes.

## Verify Steps

Not run (docs-only).

## Rollback Plan

Revert the commit(s) and restore the previous wording in AGENTS.md and role JSONs.

