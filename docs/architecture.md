# Architecture & Workflow

This document expands on the concepts referenced in `README.md` and shows how the swarm fits together.

## What Codex Swarm is (and isn’t)

- Codex Swarm is a **prompt + JSON framework** designed to run inside your IDE via the OpenAI Codex plugin.
- There is **no separate runner/daemon**: all operations are local (git + files + shell commands you run).
- It is optimized for **human-in-the-loop** workflows: plans, approvals, commits, and verification are explicit.

## Core building blocks

1. **Global rules and the ORCHESTRATOR** live in `AGENTS.md`.
2. **Specialists** live in `.codex-swarm/agents/*.json` and are dynamically loaded by the orchestrator.
3. **Tasks** live in `tasks.json` and are the canonical source of truth.
4. **Task operations and git guardrails** flow through `python scripts/agentctl.py`.
5. **Per-task workflow artifacts** live under `docs/workflow/` as `T-###.md`.

## Default agent flow (Mermaid)

The typical development workflow is: plan the task, implement it, add test coverage, document the outcome, then verify + close.

```mermaid
flowchart TD
  U[User] --> O[ORCHESTRATOR]

  O -->|Backlog + task breakdown| P[PLANNER]
  P --> TJ["tasks.json"]
  P -->|Planning artifact| D0[DOCS]
  D0 --> A0["docs/workflow/T-123.md"]

  O -->|Implementation| C[CODER]
  C -->|Test coverage handoff| T[TESTER]
  T -->|Tests/coverage suggestions| C
  C --> WC["Work commit: implementation + tests"]

  O -->|Pre-finish documentation| D1[DOCS]
  D1 -->|Update artifact| A1["docs/workflow/T-123.md"]

  O -->|Verification + closure| R[REVIEWER]
  R -->|agentctl verify/finish| DONE["Task marked DONE (tasks.json)"]
```

## Detailed agent sequence (Mermaid)

```mermaid
sequenceDiagram
  autonumber
  actor U as User
  participant O as ORCHESTRATOR
  participant P as PLANNER
  participant C as CODER
  participant T as TESTER
  participant D as DOCS
  participant R as REVIEWER
  participant A as "scripts/agentctl.py"
  participant TJ as "tasks.json"
  participant WF as "docs/workflow/T-123.md"
  participant CR as CREATOR
  participant UP as UPDATER

  U->>O: Describe goal / request (free-form)
  O->>P: Decompose goal -> tasks T-123 (+ dependencies / verify)
  P->>A: task add/update/comment (no manual edits to tasks.json)
  A->>TJ: Update backlog (checksum-backed)

  P->>D: Create planning artifact for T-123 (skeleton)
  D->>WF: Write skeleton/spec

  O-->>U: Plan + request Approval (Approve / Edit / Cancel)

  alt Approve plan
    O->>C: Implement T-123 (code/config) + prepare work commit
    C->>A: (optional) ready/start T-123 / check deps
    C->>A: guard commit T-123 -m "..." --allow PATHS
    C-->>O: Work commit ready (hash + message)

    opt Testing handoff (when appropriate)
      O->>T: Add/extend tests for affected behavior
      T-->>C: Patches/suggestions for coverage
      C->>A: guard commit T-123 -m "..." --allow PATHS
      C-->>O: Test commit (hash + message)
    end

    O->>D: Pre-finish docs update for T-123
    D->>WF: Append: what changed, how to verify, links to commits

    O->>R: Verification + closure
    R->>A: verify T-123 (commands from verify / local checks)
    R->>A: finish T-123 (mark DONE + store commit ref)
    A->>TJ: Set DONE, persist commit hash/message

    O-->>U: Summary + commit link(s)
  else Edit plan
    U-->>O: Plan edits
    O->>P: Rebuild tasks/steps based on edits
    P->>A: task update/comment
    A->>TJ: Update backlog
    O-->>U: Updated plan + re-request Approval
  else Cancel
    U-->>O: Cancel
    O-->>U: Stop with no changes
  end

  opt On-demand agent creation (if no suitable agent exists)
    P->>CR: Create new agent .codex-swarm/agents/AGENT_ID.json + workflow
    CR-->>O: Agent registered (after commit)
  end

  opt Optimization audit (only on explicit request)
    U->>O: Request to improve/optimize agents
    O->>UP: Audit .codex-swarm/agents/*.json + repo (no code changes)
    UP-->>O: Improvement plan + follow-up tasks
    O-->>U: Prioritized recommendations
  end
```

## Extending beyond development

Nothing restricts agents to “coding”. By defining workflows in JSON you can build:

- Research agents that summarize docs before implementation.
- Compliance reviewers that check diffs/commits for policy violations.
- Ops/runbook agents that coordinate repetitive procedures.
- Documentation agents that keep guides synchronized with behavior changes.
