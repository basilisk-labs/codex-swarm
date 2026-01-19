---
id: "202601131304-D4ZA6S"
title: "Add config keys and agentctl config CLI"
status: "DONE"
priority: "normal"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "dddeba676b1818a4b66c49ed91f3db1cdc47cb97", message: "✨ D4ZA6S add config-driven settings and config CLI" }
comments:
  - { author: "CODER", body: "Verified: ran python .codex-swarm/agentctl.py --help to confirm config show/set is registered; changes add config-driven defaults in agentctl and config.json." }
doc_version: 2
doc_updated_at: "2026-01-13T13:36:49+00:00"
doc_updated_by: "agentctl"
description: "Extend .codex-swarm/config.json with new settings and update agentctl to read them plus provide config show/set commands."
---
## Summary

Add config-driven settings for tasks/branch/commit and a config show/set CLI in agentctl.

## Context

User requested configurable settings in config.json plus CLI support for toggling them.

## Scope

Updated .codex-swarm/config.json with new keys and adjusted .codex-swarm/agentctl.py to read them, enforce branch/worktree prefix config, and add config show/set commands.

## Risks

Misconfigured config.json values could cause agentctl validation errors; new defaults should be verified in the repo.

## Verify Steps

python .codex-swarm/agentctl.py --help

## Rollback Plan

Revert .codex-swarm/config.json and .codex-swarm/agentctl.py to the previous commit.

## Notes

Added config keys: base_branch, paths.worktrees_dir, branch.task_prefix, tasks.id_suffix_length_default, tasks.verify.required_tags, tasks.doc sections, tasks.comments rules, commit.generic_tokens; added agentctl config show/set.

