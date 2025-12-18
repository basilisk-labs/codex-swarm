# T-086: Define workflow_mode variants (direct vs branch_pr)

## Summary

- Define `workflow_mode` values (`direct`, `branch_pr`) in shared agent rules and core docs so expectations are unambiguous.

## Goal

- Make it clear what changes operationally when `workflow_mode` switches (branches/worktrees, PR artifacts, tasks.json write rules, and who integrates/closes).

## Scope

- Documentation:
  - Clarify `workflow_mode` behavior in `AGENTS.md`, `.codex-swarm/agentctl.md`, `README.md`, and `GUIDELINE.md`.
- Agents:
  - Update key agent profiles to be explicit about `direct` vs `branch_pr` expectations.

## Risks

- Conflicting guidance across docs/agents if definitions drift; this task aligns the canonical definitions and references the config source (`.codex-swarm/swarm.config.json`).

## Verify Steps

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py pr check T-086`

## Rollback Plan

- Revert the commits for T-086 and keep the previous behavior/doc text.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.md`
- `.codex-swarm/agents/CODER.json`
- `.codex-swarm/agents/DOCS.json`
- `.codex-swarm/agents/INTEGRATOR.json`
- `.codex-swarm/agents/PLANNER.json`
- `.codex-swarm/agents/REVIEWER.json`
- `.codex-swarm/agents/TESTER.json`
- `AGENTS.md`
- `GUIDELINE.md`
- `README.md`
- `docs/workflow/T-086/README.md`
- `docs/workflow/T-086/pr/diffstat.txt`
- `docs/workflow/T-086/pr/meta.json`
- `docs/workflow/T-086/pr/review.md`
- `docs/workflow/T-086/pr/verify.log`
<!-- END AUTO SUMMARY -->
