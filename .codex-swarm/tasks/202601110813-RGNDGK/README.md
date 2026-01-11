---
id: "202601110813-RGNDGK"
title: "Harden Redmine backend and add REDMINE agent"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["redmine", "backend", "agents"]
commit: { hash: "1a5d38264519ada0bf7042c57b11a4b3464d8cad", message: "✨ RGNDGK harden redmine backend and add agent" }
comments:
  - { author: "CODER", body: "Verified: py_compile redmine backend; lint clean (owner warnings only). Added retries/cache/targeted lookup, skip invalid IDs, avoid reassignment, and created REDMINE agent." }
doc_version: 2
doc_updated_at: "2026-01-11T08:14:27+00:00"
doc_updated_by: "agentctl"
description: "Improve Redmine connector (no legacy mutations, retries, targeted lookup, safe assignee) and introduce REDMINE agent with backend-aware policies."
---
## Summary

Improve the Redmine backend (safer lookups, retries, no silent mutations, avoid reassignment) and add a REDMINE agent with backend-aware policies using only agentctl.

## Context

Redmine connector still does full scans per lookup, mutates missing task_id fields remotely, lacks retry/backoff, and forces an assignee even when one exists. We also lack an agent role to enforce Redmine-specific safety while using agentctl.

## Scope

- Add targeted task lookup in Redmine backend with cache and retry/backoff; avoid full rescan when possible.
- Remove auto-mutation of task_id for remote issues; skip invalid IDs instead.
- Respect existing assignees when writing; only set configured assignee when unassigned.
- Add simple retry/backoff for API calls with 429/5xx handling.
- Introduce REDMINE agent JSON with policies (no reassignment if assigned, use agentctl/sync, respect config fields).

## Risks

- API search by custom field may behave differently across Redmine deployments; fallback must still succeed.
- Retry/backoff could mask persistent failures if not surfaced.
- Skipping invalid task IDs may hide data inconsistencies.

## Verify Steps

- python -m py_compile .codex-swarm/backends/redmine/backend.py .codex-swarm/agentctl.py

## Rollback Plan

- Revert Redmine backend and REDMINE agent changes.

## Notes

- Keep behavior backend-agnostic for other agents; REDMINE agent documents backend expectations.

