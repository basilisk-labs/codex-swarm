---
id: "202601111048-9VBCF6"
title: "Set Redmine batch settings"
status: "TODO"
priority: "low"
owner: "CODER"
depends_on: []
tags: ["redmine", "config"]
doc_version: 2
doc_updated_at: "2026-01-11T10:49:09+00:00"
doc_updated_by: "agentctl"
description: "Set batch_size/batch_pause in redmine backend config"
---
## Summary

Set explicit batch_size (5) and batch_pause in redmine/backend.json for sync/migration throttle.

## Context

- Redmine backend now supports batching via settings; backend.json currently lacks explicit values.
- Need defaults so runs have consistent throttle without editing code.

## Scope

- Add batch_size and batch_pause to .codex-swarm/backends/redmine/backend.json.
- Use batch_size=5 tasks and a small pause for throttling.
- Do not change workflow_mode or trigger sync.

## Risks

- Too small batch or pause slows large migrations; too small pause may still hit server rate limits.

## Verify Steps

- python -m py_compile .codex-swarm/backends/redmine/backend.py

## Rollback Plan

- Revert .codex-swarm/backends/redmine/backend.json.

