# T-084: Agents: prefer agentctl CLI for supported operations

## Summary

- Make all agents “agentctl-first”: use `python scripts/agentctl.py` for any supported operation (tasks, branch/worktree, PR artifacts, verify logging, commit guardrails) and only fall back to raw commands when agentctl lacks the needed functionality.

## Goal

- Reduce manual workflow variance (especially around `tasks.json`, PR artifacts, and commits) and make agent runs faster and more predictable.

## Scope

- Update the agent prompt JSON under `.codex-swarm/agents/*.json`:
  - CODER: prefer `work start`, `pr update`, `pr note`, `verify`, and `commit` flows.
  - TESTER: prefer `verify` + `pr note` (avoid editing `verify.log` by hand).
  - REVIEWER: prefer `pr check` + `pr note` (avoid `finish`/`integrate`).
  - DOCS: prefer `task scaffold`, `pr update`, and `pr note`.
  - PLANNER/INTEGRATOR/CREATOR: explicitly state the agentctl-first rule and the fallback boundary.

## Risks

- Prompt-only change: may slightly shift agent behavior. Mitigation: keep instructions explicit and aligned with `.codex-swarm/agentctl.md`.

## Verify Steps

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py agents` (ensures JSON loads)
- Manual spot-check: open any agent JSON and confirm it instructs agentctl-first + fallback guidance.

## Rollback Plan

- Revert the agent JSON changes.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agents/CODER.json`
- `.codex-swarm/agents/CREATOR.json`
- `.codex-swarm/agents/DOCS.json`
- `.codex-swarm/agents/INTEGRATOR.json`
- `.codex-swarm/agents/PLANNER.json`
- `.codex-swarm/agents/REVIEWER.json`
- `.codex-swarm/agents/TESTER.json`
- `docs/workflow/T-084/README.md`
- `docs/workflow/T-084/pr/diffstat.txt`
- `docs/workflow/T-084/pr/meta.json`
- `docs/workflow/T-084/pr/review.md`
- `docs/workflow/T-084/pr/verify.log`
<!-- END AUTO SUMMARY -->
