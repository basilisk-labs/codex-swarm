# Overview

## What Codex Swarm Is
Codex Swarm is a local, repo-scoped framework that structures how you use the OpenAI Codex plugin inside your IDE. It adds JSON-defined agents, a task system with pluggable backends, and explicit commit rules so the work stays planned, traceable, and reviewable.

## What Codex Swarm Is Not
- Not a remote service or runner. Everything happens inside your local repo.
- Not an auto-commit bot. You stay in control of commands and commits.
- Not a replacement for your IDE. It is a workflow layer on top of it.

## Core Principles
- Local-first: no external runtime or daemon is required.
- Backend-driven truth: the canonical task source depends on the active backend.
- Traceability: every task ties back to a stable ID and a commit.
- Role clarity: each agent has a defined scope and permissions.
- Explicit approvals: plans and closures require human approval.

## Core Components
- [`AGENTS.md`](../AGENTS.md): global rules and workflow policies.
- [`.codex-swarm/agents/`](../.codex-swarm/agents/): the authoritative agent definitions.
- [`.codex-swarm/agentctl.py`](../.codex-swarm/agentctl.py): task and workflow helper CLI.
- [`.codex-swarm/backends/`](../.codex-swarm/backends/): backend plugin configs + implementations.
- [`.codex-swarm/tasks/`](../.codex-swarm/tasks/): local task storage (canonical when backend=local, cache when backend=redmine).
- [`.codex-swarm/tasks.json`](../.codex-swarm/tasks.json): exported view for local browsing and integrations.

## Where to Start
- Read [`AGENTS.md`](../AGENTS.md) for the global rules.
- Use `python .codex-swarm/agentctl.py quickstart` to see common commands.
- Start a request with the ORCHESTRATOR.

## Planned Expansions
- Add a visual summary of backend flow (local vs redmine) and canonical source switching.
- Include a short primer on the task ID format (`YYYYMMDDHHMM-<RAND>`).
- Link to backend plugin templates and configuration examples.
