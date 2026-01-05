---
id: "202601051345-MADM7W"
title: "Suffix-only commit policy, cleanup, and English-only text"
status: "TODO"
priority: "normal"
owner: "Via Mentis Assistant"
depends_on: []
tags: ["workflow", "cleanup", "policy"]
description: "Enforce suffix-only task IDs in commit subjects, remove non-English text from tracked files, update clean.sh to purge non-framework files, and refresh docs and snapshots."
---

# 202601051345-MADM7W: Suffix-only commit policy, cleanup, and English-only text

## Summary

- Enforce suffix-only task IDs in commit subjects and update docs.
- Remove non-English text from tracked files and refresh snapshots.
- Tighten clean.sh cleanup to remove non-framework files.

## Scope

- Update commit subject matching and related docs to require suffix-only IDs.
- Normalize priorities and remove Cyrillic text from tracked files.
- Adjust clean.sh cleanup targets and keep it Python 3 only.

## Risks

- Bulk text normalization touches many task README files and the tasks snapshot.
- Stricter commit checks might reject previously acceptable commit subjects.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task list --quiet`
- `python3 .codex-swarm/agentctl.py task export --out .codex-swarm/tasks.json`

## Rollback Plan

- Revert the commit and re-export tasks.json from the prior state.
