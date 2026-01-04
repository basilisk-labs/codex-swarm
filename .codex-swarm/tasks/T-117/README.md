---
id: "T-117"
title: "Remove legacy workspace directory"
status: "TODO"
priority: "med"
owner: "DOCS"
depends_on: ["T-115"]
tags: []
description: "Delete .codex-swarm/workspace after migration to .codex-swarm/tasks and update references."
---

# T-117: Remove legacy workspace directory

## Summary

- Remove the legacy `.codex-swarm/workspace/` directory after migration.
- Update references that still point to `workspace`.

## Goal

- Fully retire the old workspace layout and prevent future use.

## Scope

- Delete `.codex-swarm/workspace/`.
- Update any remaining references in docs and prompts.

## Risks

- Legacy artifacts might be lost; ensure migration is complete first.

## Verify Steps

- `rg -n \"workspace\" .codex-swarm docs README.md`

## Rollback Plan

- Restore `.codex-swarm/workspace/` from git history if needed.
