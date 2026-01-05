---
id: "202601041331-Q11MC"
title: "Prune legacy paths and optimize agentctl"
status: "TODO"
priority: "normal"
owner: "Via Mentis Assistant"
depends_on: []
tags: []
verify: null
commit: null
comments: []
description: "Remove legacy workspace/PR fallback paths (keep legacy ID reid), add task normalize, use backend export fast path, reduce redundant backend writes, add per-run task cache, and unify repeated error messaging in agentctl."
dirty: false
id_source: "custom"
redmine_id: 275
---
# 202601041331-Q11MC: Prune legacy paths and optimize agentctl

## Summary

- Remove legacy workspace and PR fallback paths from agentctl.
- Add `task normalize` to rewrite task READMEs via the backend.
- Use backend fast-path export when available.
- Reduce redundant backend writes on save/finish.
- Add per-run task cache for repeated reads.
- Unify repeated error messaging helpers.

## Goal

- Simplify agentctl by removing old path support and make core operations faster and less noisy.

## Scope

- `.codex-swarm/agentctl.py`: remove legacy path helpers, add normalize, cache, fast export, helper errors.
- `.codex-swarm/backends/local/backend.py`: helpers for normalization or hash comparison.

## Risks

- Removing legacy paths may break old repos without migration.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task normalize`
- `python3 .codex-swarm/agentctl.py task export --out .codex-swarm/tasks.json`

## Rollback Plan

- Restore `.codex-swarm/agentctl.py` and backend files from git history.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: prune legacy paths and add normalization + caching + fast export.
- `.codex-swarm/backends/local/backend.py`: helpers for normalization or hash comparison.
<!-- END AUTO SUMMARY -->
