---
id: "202601041253-0003N"
title: "Remove legacy workspace directory"
status: "DONE"
priority: "normal"
owner: "DOCS"
depends_on: ["202601041253-0003K"]
tags: []
commit: { hash: "25a6c054b1b513003186c6b337437547c6fb4a79", message: "Legacy completion (backfill)" }
doc_version: 2
doc_updated_at: "2026-01-11T08:06:07+00:00"
doc_updated_by: "agentctl"
description: "Delete .codex-swarm/workspace after migration to .codex-swarm/tasks and update references."
dirty: false
---
# 202601041253-0003N: Remove legacy workspace directory

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

## Changes Summary

- Removed `.codex-swarm/workspace/` from the repo.
- Updated references to `.codex-swarm/tasks/` in agent prompts, docs, and scripts.

