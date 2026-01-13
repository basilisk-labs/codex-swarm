---
id: "202601131728-GPGCPQ"
title: "Sync comment body with commit subject formatting"
status: "TODO"
priority: "Нормальный"
owner: "REDMINE"
depends_on: []
tags: []
verify: null
commit: null
comments: []
doc_version: 2
doc_updated_at: "2026-01-13T17:29:25+00:00"
doc_updated_by: "agentctl"
description: "Ensure comment-driven commits store the same formatted comment text used in commit subjects so length/content stay aligned and nothing is truncated across systems."
dirty: false
id_source: "custom"
---
## Summary

Normalize comment bodies used for comment-driven commits and store the normalized text in task comments to keep lengths aligned with commit subjects.

## Context

Comment-driven commit subjects are formatted from the raw comment body, which can diverge in length/content from the stored task comment; align them to avoid truncation or mismatch.

## Scope

Update agentctl comment/commit handling so formatted comment text is reused for both storage and commit subjects; document the behavior in agentctl.md.

## Risks

Normalizing comments may alter formatting for multi-line notes; keep the normalization consistent with commit subject formatting and document the change.

## Verify Steps

Manual: run a comment-driven start/block/finish and confirm the stored task comment matches the commit subject body.

## Rollback Plan

Revert the agentctl commit that normalizes stored comments to restore previous comment storage behavior.

## Notes

The normalized comment text should be identical to the commit subject body fragment produced by comment-driven commits.

