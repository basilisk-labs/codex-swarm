---
id: "202601121711-GZ15T6"
title: "Polish cleanup scripts and tasks viewer"
status: "DOING"
priority: "normal"
owner: "REDMINE"
depends_on: []
tags: ["cleanup", "ui"]
verify: null
commit: null
comments:
  - { author: "CODER", body: "Polish tasks viewer UI (iOS palette, sticky header, order toggle, tooltip tags, metadata) and update clean scripts to remove dev files." }
doc_version: 2
doc_updated_at: "2026-01-20T08:48:17+00:00"
doc_updated_by: "agentctl"
description: "Remove dev-only files in clean scripts and refine tasks viewer UI (iOS palette, order toggle, sticky header, tooltip tags, metadata) and fix layout issues."
dirty: false
id_source: "custom"
---
## Summary

Cleanup scripts remove dev-only files and tasks viewer includes sticky header, order toggle, tooltip tags, and metadata polish.

## Scope

- clean.sh/clean.ps1 remove pyproject.toml and requirements-dev.txt; tasks.html updates palette, header behavior, ordering, tooltips, and metadata.

## Risks

- UI styling regressions or layout differences across browsers.

## Verify Steps

rg -n "pyproject.toml|requirements-dev.txt" clean.sh clean.ps1\nrg -n "order-toggle|tooltip|position: sticky" .codex-swarm/viewer/tasks.html

## Rollback Plan

- Revert this commit to restore the previous tasks viewer and clean scripts.

## Notes

Implemented by later viewer/cleanup updates (202601191406-0M7XWG, 202601191414-2N28WV, 202601191433-AHRAHM) and cleanup script edits.

