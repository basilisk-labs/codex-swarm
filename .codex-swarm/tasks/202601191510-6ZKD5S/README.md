---
id: "202601191510-6ZKD5S"
title: "Document recipes prompts and wire into AGENTS"
status: "TODO"
priority: "med"
owner: "DOCS"
depends_on: ["202601191510-0AWCPY"]
tags: []
doc_version: 2
doc_updated_at: "2026-01-19T15:32:55+00:00"
doc_updated_by: "agentctl"
description: "Add .codex-swarm/RECIPES.md with global prompt guidance, reference it from AGENTS.md, and update docs/README/PRD as needed to reflect recipes CLI."
---
## Summary

Documented recipe prompt rules and updated docs to reference the new recipes CLI.

## Context

Updated .codex-swarm/RECIPES.md and referenced it from AGENTS.md, README.md, docs/README.md, docs/09-commands.md, and .codex-swarm/recipes/prd.md.

## Scope

Added global recipe prompt guidance and refreshed documentation pointers to recipes.py and inventory/bundle usage.

## Risks

Docs can drift if recipe CLI behavior changes; keep RECIPES.md aligned with recipes.py updates.

## Verify Steps

Manual review of recipe docs for correct recipes.py references.

## Rollback Plan

Revert the documentation commit for this task if the recipes guidance needs to be rolled back.

## Notes

RECIPES.md now includes outputs/artifacts guidance plus explicit bundle usage rules.

