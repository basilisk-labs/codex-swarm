# T-084: Agents: prefer agentctl CLI for supported operations

## Summary

- Update agent prompt JSON so agents default to using `python scripts/agentctl.py` whenever it supports the operation (tasks/PR artifacts/verify/commit/integrate/cleanup), falling back to raw commands only when needed.

## Goal

- Reduce inconsistent manual command usage and make runs more predictable and faster (fewer mistakes around `tasks.json`, PR artifacts, and commits).

## Scope

- `.codex-swarm/agents/*.json`: update workflows and “how to operate” sections to prefer agentctl for supported actions.
- May add short “fallback” guidance for cases where agentctl has no direct command.

## Risks

- Low. Prompt changes can shift agent behavior; keep updates minimal, explicit, and consistent with current `branch_pr` rules.

## Verify Steps

- `python scripts/agentctl.py task lint`
- Sanity: `python scripts/agentctl.py agents` still loads JSON and lists agents.

## Rollback Plan

- Revert the prompt changes.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
