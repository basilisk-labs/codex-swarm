---
id: "202601051417-P7AMW3"
title: "Remove Via Mentis ownership references"
status: "TODO"
priority: "normal"
owner: "automation"
depends_on: []
tags: ["cleanup", "policy"]
description: "Replace Via Mentis owner values with a neutral owner label across tasks and export the updated snapshot."
---

# 202601051417-P7AMW3: Remove Via Mentis ownership references

## Summary

- Replace Via Mentis owner values with a neutral owner label in task frontmatter.
- Refresh the exported tasks snapshot.

## Scope

- `.codex-swarm/tasks/*/README.md`: update owner fields.
- `.codex-swarm/tasks.json`: re-export snapshot.

## Risks

- Bulk edit touches many task records; ensure no other fields change.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task export --out .codex-swarm/tasks.json`

## Rollback Plan

- Revert the commit and re-export tasks.json from the previous state.
