---
id: "202601131307-ZR7CN1"
title: "Remove umbrella wording and clarify orchestrator planning"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-13T13:10:32+00:00"
doc_updated_by: "agentctl"
description: "Remove umbrella task mentions and rephrase instructions so the orchestrator forms a top-level plan."
---
# 202601131307-ZR7CN1: Remove umbrella wording and clarify orchestrator planning

## Summary

- Remove umbrella wording from orchestration and task rules.
- Clarify that the orchestrator forms a top-level plan before decomposition.

## Context

- User requested removing "umbrella" mentions and rephrasing instructions to emphasize top-level planning.

## Scope

- Update @AGENTS.md orchestration flow and task tracking language.
- Update @.codex-swarm/agents/ORCHESTRATOR.json outputs and workflow text.
- Update @.codex-swarm/agents/PLANNER.json outputs and workflow text.

## Risks

- Low risk: documentation-only changes.

## Verify Steps

- No tests required (doc-only change).

## Rollback Plan

- Revert the commit that updates the agent specs and AGENTS.md.

## Notes

- None.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

