---
id: "202601041346-YM3R8"
title: "Agentctl performance and UX improvements"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
description: "Add backend batch writes, fast in-memory indexes, structured error output with --json, lazy linting, and unified logging flags."
---

# 202601041346-YM3R8: Agentctl performance and UX improvements

## Summary

- Add backend batch writes and use them for normalize/finish.
- Cache task index/dependency state during a run.
- Add structured JSON error output for CI and integrations.
- Make linting lazy and opt-in for read-only commands.
- Add global logging flags for consistent verbosity.

## Goal

- Improve agentctl performance and automation ergonomics without changing core behavior.

## Scope

- `.codex-swarm/agentctl.py`: batch writes, caching, JSON error mode, lazy lint, global logging flags.
- `.codex-swarm/backends/local/backend.py`: `write_tasks()` implementation.
- `.codex-swarm/agentctl.md`: document new flags and behaviors.

## Risks

- Logging and linting behavior changes may surprise existing automation.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task normalize`
- `python3 .codex-swarm/agentctl.py task export --out .codex-swarm/tasks.json`

## Rollback Plan

- Restore `.codex-swarm/agentctl.py` and backend files from git history.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: batch writes, caching, JSON errors, lazy lint, logging flags.
- `.codex-swarm/backends/local/backend.py`: add write_tasks support.
- `.codex-swarm/agentctl.md`: document new flags.
<!-- END AUTO SUMMARY -->
