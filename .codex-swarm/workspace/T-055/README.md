# T-055: Reduce per-task commits to 3-phase workflow

## Goal

Reduce “extra” commits by standardizing on a 3-phase commit cadence per task:

1. Planning (task + initial artifact)
2. Implementation (single work commit, ideally includes tests)
3. Verification/closure (tests + review + DONE)

## Scope

- Update agent instructions in `AGENTS.md` and `.codex-swarm/agents/*.json`.
- Do not change product code or introduce new tooling.

## Files (expected)

- `AGENTS.md`
- `.codex-swarm/agents/PLANNER.json`
- `.codex-swarm/agents/CODER.json`
- `.codex-swarm/agents/TESTER.json`
- `.codex-swarm/agents/DOCS.json`
- `.codex-swarm/agents/REVIEWER.json`

## Verification

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py agents`

## Implementation Notes

- Updated commit guidance to a default 3-phase cadence (planning, implementation, verification/closure).
- Aligned agent workflows to avoid extra status-only commits:
  - TESTER: no commit by default; provide test changes for CODER to include in the implementation commit.
  - DOCS: artifacts/docs committed as part of planning or final closure (unless doc-only).
  - REVIEWER: closes tasks with a single final commit (docs artifact + `tasks.json`), with `finish --commit <implementation_commit>`.
