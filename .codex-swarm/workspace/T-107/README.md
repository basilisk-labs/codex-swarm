# T-107: Link file references in docs

## Summary

- Converted file references in docs to GitHub-friendly links.

## Goal

- Make documentation references clickable and consistent.

## Scope

- Update docs/*.md to link to referenced files and folders.

## Risks

- Low: docs-only changes.

## Verify Steps

- Manual review (docs-only change).

## Rollback Plan

- Revert this task's commits.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- docs/README.md: link the index, source-of-truth, and help references.
- docs/agents.md: link AGENTS and agents directory.
- docs/overview.md: link core components and AGENTS.
- docs/workflow.md: link .codex-swarm/tasks.json references.
- docs/branching-and-pr-artifacts.md: link config, tasks, and PR artifact paths.
- docs/tasks-and-agentctl.md: link .codex-swarm/tasks.json.
- docs/troubleshooting.md: link .codex-swarm/tasks.json.
- docs/glossary.md: link tasks.json and workspace paths.
- docs/architecture.md: link README and core paths.
<!-- END AUTO SUMMARY -->
