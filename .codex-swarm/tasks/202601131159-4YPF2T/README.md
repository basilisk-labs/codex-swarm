---
id: "202601131159-4YPF2T"
title: "Auto-commit on finish via config"
status: "DOING"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
comments:
  - { author: "ORCHESTRATOR", body: "Start: add config-driven auto status commit on finish and document the behavior." }
doc_version: 2
doc_updated_at: "2026-01-13T12:00:23+00:00"
doc_updated_by: "agentctl"
description: "Add a config option to auto-run finish status commits, update agentctl behavior and docs, and enable the setting in config.json."
---
## Summary

Add a config-controlled auto status commit for finish and document the behavior.

## Context

User wants finish to commit task updates automatically when configured.

## Scope

Add a config flag, wire it into agentctl finish, update docs, and enable it in .codex-swarm/config.json.

## Risks

Low risk; incorrect config parsing could block finish or trigger unexpected commits.

## Verify Steps

No tests (behavior verified by inspection).

## Rollback Plan

Revert the commit and remove the config flag from config.json.

