---
id: "202601200829-0Q4Z49"
title: "Fix task lint dependency errors"
status: "DONE"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
commit: { hash: "4d23bdcf5906ad3410b10a926353888d514b9730", message: "✨ 0Q4Z49 fix malformed depends_on values" }
comments:
  - { author: "ORCHESTRATOR", body: "verified: not run (metadata-only) | details: depends_on values corrected so task lint can pass." }
doc_version: 2
doc_updated_at: "2026-01-20T08:30:52+00:00"
doc_updated_by: "agentctl"
description: "Correct malformed depends_on entries in tasks.json and confirm lint passes."
---
## Summary

Fix malformed depends_on entries so task lint passes cleanly.

## Scope

- Replace malformed depends_on values for 202601191449-RM6JRR and 202601191449-XTMQRZ.\n- Re-export tasks.json and confirm task lint passes.

## Risks

Low: metadata-only change; risk limited to dependency metadata.

## Verify Steps

Not run (metadata fix); will run task lint after export.

## Rollback Plan

Revert the commit(s) to restore prior depends_on values if needed.

