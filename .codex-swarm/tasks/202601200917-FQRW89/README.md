---
id: "202601200917-FQRW89"
title: "Update ORCHESTRATOR for global recipes bundle"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["agents", "recipes"]
doc_version: 2
doc_updated_at: "2026-01-20T09:18:12+00:00"
doc_updated_by: "agentctl"
description: "Update ORCHESTRATOR workflow to refresh the global recipes bundle on startup."
---
## Summary

Update ORCHESTRATOR workflow to refresh the global recipes bundle on startup.

## Context

Global bundle should stay current and be refreshed explicitly at run start.

## Scope

- Update ORCHESTRATOR.json to run recipes.py bundle build with confirmation.

## Risks

Wording could imply implicit tool execution; must keep explicit confirmation.

## Verify Steps

Review ORCHESTRATOR.json for updated instructions.

## Rollback Plan

Revert ORCHESTRATOR.json changes.

