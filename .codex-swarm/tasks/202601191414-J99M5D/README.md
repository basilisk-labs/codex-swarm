---
id: "202601191414-J99M5D"
title: "Viewer data aggregation"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: ["[\"202601191414-4ZX6FD\"]"]
tags: []
doc_version: 2
doc_updated_at: "2026-01-19T14:20:19+00:00"
doc_updated_by: "agentctl"
description: "Add any backend/API or client aggregation needed for dashboards using tasks.json and agents.json."
---
## Summary

Wire data aggregation for dashboard metrics using existing task fields.

## Context

The viewer can derive counts and breakdowns from tasks.json without new storage, but needs client logic to normalize fields consistently.

## Scope

- Extend normalization to include doc/id_source/dirty metadata.
- Add aggregation helpers and dashboard rendering logic.

## Risks

Risk: missing or inconsistent fields could skew metrics; handle empty values gracefully.

## Verify Steps

- Spot-check dashboard counts against visible task list and filters.

## Rollback Plan

Revert dashboard aggregation logic in `.codex-swarm/viewer/tasks.html`.

## Notes

Avoid new API endpoints unless required for performance.

