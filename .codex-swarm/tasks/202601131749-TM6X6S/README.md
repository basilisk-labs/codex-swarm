---
id: "202601131749-TM6X6S"
title: "Switch tasks backend to local"
status: "DONE"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
commit: { hash: "57bea995c00b60ad744af0215db1b368883c7b06", message: "✅ 9PQ5D2 verified: formatting-only change in .codex-swarm/config.json | details: task docs updated; no tests run." }
comments:
  - { author: "ORCHESTRATOR", body: "verified: config already set to local backend | details: task was a no-op, no tests run." }
doc_version: 2
doc_updated_at: "2026-01-13T17:50:47+00:00"
doc_updated_by: "agentctl"
description: "Restore the tasks backend setting to use the local backend config so agentctl operates on local tasks again."
---
## Summary

Set tasks_backend.config_path to the local backend config so agentctl uses local task storage.

## Context

Requested to switch the task backend settings back to local.

## Scope

Updated tasks_backend.config_path in .codex-swarm/config.json to point at .codex-swarm/backends/local/backend.json.

## Risks

Low risk: only the backend selection changed. Risk is that workflows expecting the Redmine backend will now read/write local tasks instead.

## Verify Steps

python .codex-swarm/agentctl.py config show

## Rollback Plan

Run: python .codex-swarm/agentctl.py config set tasks_backend.config_path .codex-swarm/backends/redmine/backend.json

## Notes

Initial task creation timed out while the backend was set to Redmine; after switching to local, task creation succeeded.

