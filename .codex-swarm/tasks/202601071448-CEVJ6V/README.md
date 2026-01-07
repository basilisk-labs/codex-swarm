---
id: "202601071448-CEVJ6V"
title: "Improve agentctl task output context"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["agentctl", "cli", "tasks"]
doc_version: 2
doc_updated_at: "2026-01-07T14:48:55+00:00"
doc_updated_by: "agentctl"
description: "Enhance agentctl CLI outputs to include richer task context (readiness, deps, metadata) to reduce extra checks."
---
## Summary

Improve agentctl CLI outputs to include richer task context (deps, readiness, metadata) so agents need fewer follow-up commands.

## Scope

- Enrich task list/show/ready outputs with dependency readiness and metadata.\n- Keep outputs compact and stable for CLI use.

## Risks

- More verbose output may affect scripts that parse human-readable CLI output.

## Verify Steps

- Run 'python .codex-swarm/agentctl.py task show <task-id>' and 'python .codex-swarm/agentctl.py task list' to confirm richer context.

## Rollback Plan

Revert agentctl output changes if verbosity breaks downstream scripting.

