---
id: "202601041253-0003S"
title: "agentctl: preserve frontmatter on scaffold overwrite"
status: "DONE"
priority: "normal"
owner: "Via Mentis Assistant"
depends_on: []
tags: []
verify: null
commit: "e571744e288fc0f63599967eae460d290d4c97ef"
comments: []
description: "Keep the frontmatter block intact when overwriting task README scaffolds."
dirty: false
id_source: "custom"
redmine_id: 280
---
# 202601041253-0003S: agentctl: preserve frontmatter on scaffold overwrite

## Summary

- Preserve frontmatter when `task scaffold --overwrite` rewrites task READMEs.

## Goal

- Avoid losing the frontmatter block in `.codex-swarm/tasks/<task-id>/README.md` during overwrite scaffolds.

## Scope

- Update `agentctl` scaffold to retain existing frontmatter and reapply the template body.

## Risks

- Edge-case frontmatter parsing might miss malformed headers.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task scaffold 202601041253-0003S --overwrite`
- Confirm the frontmatter block remains at the top of `.codex-swarm/tasks/202601041253-0003S/README.md`.

## Rollback Plan

- Revert the scaffold changes in `.codex-swarm/agentctl.py`.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.py`: preserve frontmatter when overwriting task scaffolds.
<!-- END AUTO SUMMARY -->