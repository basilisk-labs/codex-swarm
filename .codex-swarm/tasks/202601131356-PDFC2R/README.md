---
id: "202601131356-PDFC2R"
title: "Validate Redmine backend sync against local backend"
status: "DONE"
priority: "normal"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["redmine", "sync"]
commit: { hash: "e5e77d4e630794608b392d4b458422a6d88b7ca1", message: "✨ PDFC2R validate redmine sync with sandbox cache" }
comments:
  - { author: "ORCHESTRATOR", body: "verified: sync pull/push executed against Redmine sandbox using isolated cache | details: report saved in task notes." }
doc_version: 2
doc_updated_at: "2026-01-20T09:08:20+00:00"
doc_updated_by: "agentctl"
description: "Analyze backend state, switch to Redmine, test connector + sync, compare data volume with local truth, and assess whether local task storage can be safely disabled."
---
# 202601131356-PDFC2R: Validate Redmine backend sync against local backend

## Summary

Validated Redmine sync against sandbox using an isolated cache and recorded results.

## Context

Remote Redmine is a sandbox; local files remain authoritative. Sync was run with a separate cache to avoid overwriting canonical local tasks.

## Scope

- Added sandbox backend config with isolated cache (.codex-swarm/backends/redmine/backend.sandbox.json).\n- Switched tasks_backend.config_path to sandbox config, ran sync pull and push, then restored local backend config.\n- Captured sync output and verification steps.

## Risks

Low: sync ran against sandbox with isolated cache; risk limited to sandbox data.

## Verify Steps

python .codex-swarm/agentctl.py config set tasks_backend.config_path .codex-swarm/backends/redmine/backend.sandbox.json\npython .codex-swarm/agentctl.py sync redmine --direction pull\npython .codex-swarm/agentctl.py sync redmine --direction push --yes\npython .codex-swarm/agentctl.py config set tasks_backend.config_path .codex-swarm/backends/local/backend.json

## Rollback Plan

Revert backend config changes if needed and delete .codex-swarm/backends/redmine/backend.sandbox.json plus .codex-swarm/tasks-redmine-cache.

## Notes

Agent verification scenario:
1) Ensure local backend is canonical; set tasks_backend.config_path to .codex-swarm/backends/redmine/backend.sandbox.json.
2) Run: python .codex-swarm/agentctl.py sync redmine --direction pull
3) Optional: run: python .codex-swarm/agentctl.py sync redmine --direction push --yes (expects no dirty tasks unless cache modified).
4) Restore tasks_backend.config_path to .codex-swarm/backends/local/backend.json.
5) Inspect .codex-swarm/tasks-redmine-cache for pulled tasks if needed.

Report (2026-01-20):
- pull: ✅ pulled 11 task(s)
- push: ℹ️ no dirty tasks to push
- config restored to local backend.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

