---
id: "202601201257-ZA4XF2"
title: "Ignore new files during agent work"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-20T12:58:42+00:00"
doc_updated_by: "agentctl"
description: "Update agent instructions so agents ignore newly added files and only work/commit their own changes."
---
## Summary

Update AGENTS.md to instruct all agents to ignore new/untracked files not created by them and to only work on/commit their own changes.

## Scope

Add a global rule in AGENTS.md covering new/untracked files and commit scope.

## Risks

Low risk; behavior change may reduce visibility into unexpected additions, but agents will still focus on their own changes.

## Verify Steps

No automated tests required; verify AGENTS.md contains the new rule.

## Rollback Plan

Revert the AGENTS.md change that adds the new files rule.

