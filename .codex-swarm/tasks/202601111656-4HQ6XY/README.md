---
id: "202601111656-4HQ6XY"
title: "Add strict Python linting/formatting and cleanup"
status: "DOING"
priority: "high"
owner: "CODER"
depends_on: []
tags: ["python", "lint", "quality", "tooling"]
comments:
  - { author: "CODER", body: "Start: Add strict Python lint/format/type-check configs, update code to pass them, and clean new artifacts." }
doc_version: 2
doc_updated_at: "2026-01-11T16:57:04+00:00"
doc_updated_by: "agentctl"
description: "Introduce strict Python lint/format/type-check tooling, update cleanup scripts for new artifacts, and ensure the repo passes the checks."
---
## Summary

Add strict Python lint/format/type-check tooling, clean up their artifacts, and ensure repository Python code passes the new checks.

## Context

User requested максимально жесткие линтеры/фиксеров for Python and cleanup of their artifacts; tooling should keep code correct and verified after linting.

## Scope

Add lint/format/type-check configs (ruff + type checker), update Python code to comply, add ignore/clean rules for caches, and document/run verify commands.

## Risks

Strict rules may require code refactors or per-file ignores; type-checker strictness can surface missing annotations or third-party stubs.

## Verify Steps

ruff format .\nruff check .\nmypy .

## Rollback Plan

Revert lint config files, clean script changes, and any code edits; remove lint dependencies; rerun previous checks.

## Notes

Aim for strict linting while scoping unavoidable exceptions (e.g., CLI subprocess usage).

