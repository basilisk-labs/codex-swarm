---
id: "202601072146-7CZMM7"
title: "Remove clean.ps1 at end of clean.sh"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "67184b29e967919d6c60b058ff6eef0e1f5fe734", message: "рџ› пёЏ 7CZMM7 remove clean.ps1 at end of clean.sh" }
comments:
  - { author: "INTEGRATOR", body: "Verified: not run; repo has no automated tests for shell scripts (manual verification not performed)." }
doc_version: 2
doc_updated_at: "2026-01-07T21:48:10+00:00"
doc_updated_by: "agentctl"
description: "Update clean.sh to delete clean.ps1 at the end so cleanup removes both scripts consistently."
---
## Summary

Ensure clean.sh removes clean.ps1 at the end of cleanup.

## Context

clean.ps1 is now tracked; clean.sh should remove it during cleanup.

## Scope

- Update clean.sh to delete clean.ps1 at the end.\n- No other cleanup behavior changes.

## Risks

Low. Adds one more file removal at script end.

## Verify Steps

Not run (no automated tests for shell scripts in this repo).

## Rollback Plan

Revert commit 67184b29e967 to remove the clean.ps1 deletion line.

## Notes

No tests run; direct workflow mode in use.

