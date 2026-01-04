---
id: "202601041253-0003M"
title: "Agents: export tasks.json on close"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: ["202601041253-0003K"]
tags: []
commit: { hash: "188350307b487d91a3ef004847f87f8b6d1a3995", message: "🛠️ 0003M export tasks.json on close" }
description: "Update agent prompts to require tasks.json export after finish/closure and align task source-of-truth wording with backend model."
dirty: false
redmine_id: 390
---
# 202601041253-0003M: Agents: export tasks.json on close

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

## Changes Summary

- Updated agent prompts to treat `tasks.json` as a snapshot and export it after closure.
- Aligned backend wording across AGENTS and agent JSONs.
