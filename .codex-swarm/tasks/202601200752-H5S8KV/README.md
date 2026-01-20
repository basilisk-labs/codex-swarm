---
id: "202601200752-H5S8KV"
title: "Update ORCHESTRATOR recipe bundle refresh"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["agents", "recipes", "workflow"]
doc_version: 2
doc_updated_at: "2026-01-20T08:12:10+00:00"
doc_updated_by: "agentctl"
description: "Require ORCHESTRATOR to refresh recipes inventory and bundle.json at run start when recipes are involved (after plan approval)."
---
## Summary

Update ORCHESTRATOR workflow to refresh recipe bundle.json at run start with explicit confirmation.

## Context

User expects the orchestrator to keep recipe bundles fresh while still honoring the rule that tool execution requires confirmation.

## Scope

- Update .codex-swarm/agents/ORCHESTRATOR.json workflow to include recipes.py scan and compile before execution.
- Reference bundle.json location under .codex-swarm/.runs/<run-id>/.

## Risks

The new step could be misread as an implicit tool run; it must explicitly require confirmation.

## Verify Steps

Review ORCHESTRATOR.json to confirm the added workflow step is accurate and constrained.

## Rollback Plan

Revert the JSON change.

## Notes

No runtime behavior changes implemented in code.

