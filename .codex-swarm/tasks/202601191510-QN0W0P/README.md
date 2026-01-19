---
id: "202601191510-QN0W0P"
title: "Analyze recipes PRD and implementation notes"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-19T15:13:05+00:00"
doc_updated_by: "agentctl"
description: "Review the recipes PRD, map requirements to CLI/doc updates, and record implementation notes needed for execution."
---
## Summary

Reviewed the recipes PRD and mapped core CLI + documentation deliverables for implementation.

## Context

Sources reviewed: .codex-swarm/recipes/prd.md; repository currently has no recipes CLI or recipe manifests beyond the PRD.

## Scope

Define requirements for recipes CLI commands (scan/show/compile/explain), manifest normalization (v1 + legacy), bundle/context assembly, and documentation additions (RECIPES.md + AGENTS.md + README/prd updates).

## Risks

Context scanning could exceed size limits without strict enforcement; minimal schema validation may drift from full JSON Schema; path template sanitization must block unsafe values.

## Verify Steps

None (analysis-only task).

## Rollback Plan

Revert the analysis notes commit for this task if the PRD mapping needs to be removed or replaced.

## Notes

Key requirements: inventory generation from .codex-swarm/recipes/*/manifest.json; compile bundles with context policy + tool plan; support legacy manifest mapping; add RECIPES.md and wire into AGENTS.md; create new .codex-swarm/recipes.py CLI without network or task writes.

