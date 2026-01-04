---
id: "T-116"
title: "Agents: export tasks.json on close"
status: "TODO"
priority: "med"
owner: "DOCS"
depends_on: ["T-115"]
tags: []
description: "Update agent prompts to require tasks.json export after finish/closure and align task source-of-truth wording with backend model."
---

# T-116: Agents: export tasks.json on close

## Summary

- Update agent prompts so closures regenerate `tasks.json`.
- Align task source-of-truth wording with backend routing.

## Goal

- Ensure the closing agent exports `tasks.json` after `finish`, keeping snapshots in sync.

## Scope

- Update agent JSON prompts and `AGENTS.md` where they mention `tasks.json` as canonical.
- Add a closure checklist entry to export the snapshot.

## Risks

- Prompt drift if docs and agent JSONs are not updated together.

## Verify Steps

- `rg -n \"tasks.json\" .codex-swarm/agents AGENTS.md`

## Rollback Plan

- Revert prompt updates in `.codex-swarm/agents/*.json` and `AGENTS.md`.
