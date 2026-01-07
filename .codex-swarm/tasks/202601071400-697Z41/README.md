---
id: "202601071400-697Z41"
title: "Standardize task README format + agentctl-only updates"
status: "TODO"
priority: "normal"
owner: "automation"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-07T14:21:19+00:00"
doc_updated_by: "agentctl"
description: "Refine task README.md format for human/agent readability and enforce updates via agentctl commands only."
---
# 202601071400-697Z41: Standardize task README format + agentctl-only updates

## Summary

- Add Context/Notes sections to task README template.
- Add agentctl doc section updates + metadata guard for README changes.
- Update local backend to stamp doc metadata.

## Context

- Agents should not edit task READMEs by hand; agentctl must own updates.
- README structure should balance required metadata with readable guidance.

## Scope

- Update agentctl README template and doc section commands.
- Add guardrails that require agentctl doc metadata for staged task READMEs.
- Update local backend to maintain doc metadata and docs/instructions.
- Extend Redmine backend field mapping to store doc metadata and comments.

## Risks

- Guard may block commits that touch legacy task READMEs missing doc metadata until updated via agentctl.
- Section parsing is heading-based; unusual heading formats may be ignored.

## Verify Steps

- python -m py_compile .codex-swarm/agentctl.py .codex-swarm/backends/local/backend.py .codex-swarm/backends/redmine/backend.py

## Rollback Plan

- Revert the commit and re-run agentctl if needed.

## Notes

- Existing READMEs keep their content; metadata is added on first agentctl update.
- Redmine needs custom fields for comments/doc metadata to keep parity with local.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

