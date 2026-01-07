# Architecture

## Summary
Codex Swarm is a local workflow layer that combines JSON-defined agents, a pluggable task backend, and explicit commit rules. The canonical architecture and workflow diagrams live in [`README.md`](../README.md) under **Architecture & Workflow**.

## Key Concepts
- Global rules are defined in [`AGENTS.md`](../AGENTS.md).
- Agents are defined in [`.codex-swarm/agents/`](../.codex-swarm/agents/).
- Task source-of-truth is backend-driven (local folder or Redmine).
- Local task storage lives under [`.codex-swarm/tasks/`](../.codex-swarm/tasks/) and doubles as a cache when backend=redmine.
- Backend plugin configs live under [`.codex-swarm/backends/`](../.codex-swarm/backends/).
- `tasks.json` is an exported view for local browsing and integrations.

## Architectural Layers
1. **Agent layer:** Orchestrator + specialist agents from `.codex-swarm/agents/`.
2. **Workflow layer:** `agentctl` CLI enforces guardrails and routes task ops to the active backend.
3. **Backend layer:** pluggable task storage (local or Redmine), with auto offline fallback when Redmine is unavailable.
4. **Export layer:** `tasks.json` generated from the canonical backend for local tooling like `.codex-swarm/viewer/tasks.html`.

## Where to Read Next
- [`README.md`](../README.md) for diagrams and the full architecture narrative.
- [`05-workflow.md`](05-workflow.md) for end-to-end process details.
- [`07-tasks-and-backends.md`](07-tasks-and-backends.md) for backend behavior and the task ID format.
- [`08-branching-and-pr-artifacts.md`](08-branching-and-pr-artifacts.md) for `workflow_mode` specifics.

## Planned Expansions
- Add a sequence diagram for auto offline fallback and sync.
- Document the backend plugin loading path and validation rules.
