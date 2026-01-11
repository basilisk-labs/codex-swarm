---
id: "202601111732-M23S62"
title: "Refactor agentctl/backends for strict mypy"
status: "TODO"
priority: "high"
owner: "CODER"
depends_on: ["202601111656-4HQ6XY"]
tags: ["python", "mypy", "refactor", "typing", "agentctl", "backend"]
verify: [".venv/bin/ruff format .", ".venv/bin/ruff check .", ".venv/bin/mypy"]
comments:
  - { author: "CODER", body: "Plan: add refactor task for strict mypy in agentctl/backends and schedule GitHub sync + cleanup update task." }
doc_version: 2
doc_updated_at: "2026-01-11T17:33:08+00:00"
doc_updated_by: "agentctl"
description: "Refactor agentctl and backend modules to pass strict mypy without exclusions while preserving behavior."
---
## Summary

Refactor agentctl/backends to satisfy strict mypy without exclusions while preserving CLI behavior.

## Scope

- Audit mypy errors in agentctl/backends and map fixes.
- Add typed helpers (TypedDict/Protocol/dataclasses) for task models and backend APIs.
- Narrow dynamic imports and casts so mypy can validate module loading.
- Remove mypy excludes for agentctl/backends in pyproject.toml.

## Risks

- Type refactors may change CLI edge cases or backend error handling.
- Large surface area could require incremental migration to avoid regressions.

## Verify Steps

- .venv/bin/ruff format .
- .venv/bin/ruff check .
- .venv/bin/mypy

## Rollback Plan

- ...

## Notes

Aim for incremental, well-tested typing improvements rather than broad rewrites.

