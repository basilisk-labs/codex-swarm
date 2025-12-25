# T-056: Add Mermaid agent workflow diagram to README

## Goal

Add a concise workflow description and a Mermaid flowchart diagram to `README.md` describing the default agent handoff sequence and the 3-phase commit cadence.

## Scope

- Update `README.md` only (plus this workflow artifact).

## Diagram requirements

- Must show the typical sequence:
  - ORCHESTRATOR → PLANNER → (DOCS planning artifact) → CODER → TESTER → DOCS → REVIEWER → DONE
- Must mention the 3-phase commits at a high level (planning / implementation / verification+closure).

## Verification

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py agents`

## Implementation Notes

- Added a Mermaid flowchart section to `README.md` describing the default agent handoffs and the typical dev workflow sequence.
- Updated the README agent table entry for DOCS to mention workflow artifacts under `.codex-swarm/workspace/`.
