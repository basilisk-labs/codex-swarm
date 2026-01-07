---
id: "202601071438-C7W2GE"
title: "Update Redmine custom field IDs"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["redmine", "backend", "docs"]
doc_version: 2
doc_updated_at: "2026-01-07T14:38:42+00:00"
doc_updated_by: "agentctl"
description: "Update Redmine backend config and docs to use sequential custom field IDs 1-8 for task metadata."
---
## Summary

Update Redmine custom field ID mapping to use sequential IDs 1-8 for task metadata.

## Scope

- Update Redmine backend config custom_fields mapping to 1..8.\n- Update Redmine docs/examples with the same mapping.

## Risks

- If Redmine custom field IDs differ, sync will fail until corrected.

## Verify Steps

- (optional) Use Redmine admin UI to confirm custom field IDs.\n- Run agentctl sync with Redmine once configured.

## Rollback Plan

Revert the Redmine backend config and docs to the previous custom field IDs.

