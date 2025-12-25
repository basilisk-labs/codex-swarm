# T-103: Update GitHub sync scripts for new .codex-swarm structure

## Summary

- Updated GitHub sync script and workflow to use .codex-swarm/tasks.json.

## Goal

- Keep GitHub automation aligned with the current repo layout.

## Scope

- Point sync script to .codex-swarm/tasks.json.
- Update workflow path filter and step label.

## Risks

- Low: workflow and sync script path update only.

## Verify Steps

- Manual review (GitHub workflow not executed locally).

## Rollback Plan

- Revert this task's commits to restore prior workflow/script paths.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- .github/scripts/sync_tasks.py: use .codex-swarm/tasks.json as source of truth.
- .github/workflows/sync-tasks.yml: watch .codex-swarm/tasks.json and update step label.
<!-- END AUTO SUMMARY -->
