---
id: "202601200757-DVXJJ7"
title: "Agentctl preflight warnings for workflow_mode + PR artifacts"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["agentctl", "workflow"]
commit: { hash: "4d6d802bc749080310d8b289b3c4612efe1cfc68", message: "✨ DVXJJ7 warn on direct-mode PR usage and stale meta" }
comments:
  - { author: "CODER", body: "verified: not run | details: manual review only for warning paths in agentctl pr commands and pr_check." }
doc_version: 2
doc_updated_at: "2026-01-20T08:20:55+00:00"
doc_updated_by: "agentctl"
description: "Add lightweight preflight checks/warnings for direct vs branch_pr mismatches and missing PR artifact updates."
---
## Summary

Add preflight warnings for workflow_mode mismatches and stale PR artifacts in agentctl.

## Scope

- Warn when running pr open/update/check/note in workflow_mode=direct.\n- Warn when pr_check detects stale or missing PR meta head_sha.

## Risks

Low: warnings only; no behavior changes to success/failure paths.

## Verify Steps

Not run (manual inspection only).

## Rollback Plan

Revert the commit(s) to remove the warning hooks in agentctl.

