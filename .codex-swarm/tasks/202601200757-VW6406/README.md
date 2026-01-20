---
id: "202601200757-VW6406"
title: "Add task README/comment templates and workflow checklists"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: []
tags: ["docs", "workflow"]
commit: { hash: "4ca627e3dc386c1349747199e507fc94df337988", message: "✨ VW6406 add workflow templates and checklists" }
comments:
  - { author: "DOCS", body: "verified: not run (docs-only) | details: added templates and checklists in docs/05-workflow.md." }
doc_version: 2
doc_updated_at: "2026-01-20T08:17:44+00:00"
doc_updated_by: "agentctl"
description: "Provide templates for required task README sections and status comments, plus direct/branch_pr checklists to reduce workflow errors."
---
## Summary

Add README section templates, status comment templates, and workflow checklists to reduce task/doc errors.

## Scope

- Add template guidance for required task README sections.\n- Add status comment templates (Start/Blocked/Verified).\n- Add direct/branch_pr checklists in workflow docs.

## Risks

Low: documentation-only changes; risk is outdated guidance if workflows shift.

## Verify Steps

Not run (docs-only).

## Rollback Plan

Revert the commit(s) and remove the templates/checklists from workflow docs.

