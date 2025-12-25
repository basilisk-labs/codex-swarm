# Architecture

## Summary
Codex Swarm is a local workflow layer that combines JSON-defined agents, a task backlog, and explicit commit rules. The canonical architecture and workflow diagrams live in `README.md` under **Architecture & Workflow**.

## Key Concepts
- Global rules are defined in `AGENTS.md`.
- Agents are defined in `.codex-swarm/agents/*.json`.
- Tasks live in `.codex-swarm/tasks.json`.
- Task artifacts live under `.codex-swarm/workspace/`.

## Where to Read Next
- `README.md` for diagrams and the full architecture narrative.
- `workflow.md` for end-to-end process details.
- `branching-and-pr-artifacts.md` for `workflow_mode` specifics.
