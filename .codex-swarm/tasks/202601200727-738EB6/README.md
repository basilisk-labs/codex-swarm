---
id: "202601200727-738EB6"
title: "Harden agent task pipeline"
status: "DONE"
priority: "normal"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["workflow", "agentctl"]
commit: { hash: "5d997712de3cb15644dd93f2eda82dc12d71f0f4", message: "✨ 738EB6 harden task pipeline: strict allowlist, duplicate-title guard, docs updates" }
comments:
  - { author: "ORCHESTRATOR", body: "verified: guard scope and stricter allowlist flow documented | details: no automated tests run." }
doc_version: 2
doc_updated_at: "2026-01-20T07:43:36+00:00"
doc_updated_by: "agentctl"
description: "Reduce accidental file staging, prevent duplicate tasks, and clarify agentctl task doc mutations in agent workflows and tooling."
---
## Summary

- Tighten staging/commit guardrails to prevent accidental file inclusion.
- Block duplicate active task titles unless explicitly overridden.
- Document agentctl-managed README metadata updates for agents.

## Context

- Agents were frequently staging extra files, creating duplicate tasks, and misattributing README metadata changes.

## Scope

- Add `guard scope` to fail when changes exist outside an allowlist.
- Switch auto-allow to file-level and require explicit `--commit-auto-allow`.
- Add duplicate-title detection to `task new` with `--allow-duplicate` override.
- Update agent/docs guidance to use strict allowlists and expect README metadata updates.

## Risks

- Stricter guardrails may block workflows that relied on implicit auto-allow.
- Duplicate-title detection can prevent legitimate reuse of titles without `--allow-duplicate`.

## Verify Steps

- Not run (manual review only).

## Rollback Plan

- Revert the commits for this task to restore previous guard/allowlist behavior.

## Notes

- This task intentionally prioritizes safety over convenience.

