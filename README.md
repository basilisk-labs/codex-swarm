![Codex Swarm Header](assets/header.png)

# Codex Swarm

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

Codex Swarm turns your local IDE + OpenAI Codex plugin into a predictable multi-agent workflow. It fixes the “just chat with the model” chaos by adding a small, opinionated layer: JSON-defined agents, a shared task backlog, and commit rules so every change is planned and traceable. There is no separate runner or daemon—everything lives in this repo and flows through the plugin you already use.

## Getting Started

Prerequisites:
- OpenAI Codex plugin (Cursor / VS Code / JetBrains) configured for your repo
- Git and Python 3.10+ installed locally

1. Clone the repo and open it in your IDE:
   ```bash
   git clone https://github.com/basilisk-labs/codex-swarm.git
   cd codex-swarm
   ```

2. Start with the ORCHESTRATOR:
   - Describe a goal (e.g. “Add a new agent that keeps CHANGELOG.md in sync”).
   - The ORCHESTRATOR will propose a plan, map steps to agents (PLANNER/CODER/TESTER/DOCS/REVIEWER), and ask for approval.

3. Task tracking:
   - `tasks.json` is the single source of truth.
   - Use `python scripts/agentctl.py task list` / `python scripts/agentctl.py task show T-123` to inspect tasks.
   - Use `python scripts/agentctl.py task lint` to validate schema/deps/checksum (manual edits are not allowed).

4. Optional (clean slate):
   - Run `./clean.sh` to remove framework-development artifacts and reinitialize git, leaving only the minimal “runtime” files needed to reuse Codex Swarm as your own local project.

## Example: auto-doc for a tiny refactor

1. User: “Refactor utils/date.ts and update the README accordingly.”
2. ORCHESTRATOR: proposes a 2-step plan (PLANNER creates tasks; CODER implements and commits).
3. PLANNER: creates T-041 (refactor) and T-042 (docs) and sets them to DOING.
4. CODER: edits `utils/date.ts`, updates `README.md`, runs any checks, and commits with an emoji message like “🔧 T-041 refactor date utils”.
5. REVIEWER: verifies the diff, adds a short review comment, and marks T-041 done.
6. DOCS (optional): updates docs for T-042 and marks it done.

## ✨ Highlights

- 🧠 **Orchestrated specialists:** Every agent prompt lives in `.codex-swarm/agents/*.json` so the orchestrator can load roles, permissions, and workflows dynamically.
- 🧭 **Workflow guardrails:** The global instructions in `AGENTS.md` enforce approvals, planning, and emoji-prefixed commits so collaboration stays predictable.
- 📝 **Docs-first cadence:** `tasks.json` drives the backlog, and `python scripts/agentctl.py` provides a safe CLI for inspecting/updating tasks (checksum-backed, no manual edits).
- 🧪 **Post-change test coverage:** Development work can hand off to TESTER so relevant behavior is protected by automated tests before moving on.

## 📚 Docs index

- `GUIDELINE.md`: Framework usage guidelines (day-to-day workflow).
- `.codex-swarm/agentctl.md`: `agentctl` quick reference (task ops + git guardrails).
- `docs/architecture.md`: How the swarm works (concepts + Mermaid diagrams).
- `CONTRIBUTING.md`: How to propose changes and work with maintainers.
- `CODE_OF_CONDUCT.md`: Community expectations and reporting.

## 🗂️ Repository Layout

```
.
├── AGENTS.md
├── .codex-swarm
│   ├── agentctl.md
│   ├── swarm-config.json
│   └── agents
│       ├── PLANNER.json
│       ├── CODER.json
│       ├── TESTER.json
│       ├── REVIEWER.json
│       ├── DOCS.json
│       ├── CREATOR.json
│       └── UPDATER.json
├── clean.sh
├── LICENSE
├── README.md
├── tasks.json
├── tasks.html
├── docs
│   ├── architecture.md
│   └── workflow
│       └── T-123.md
├── scripts
│   └── agentctl.py
```

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | 🌐 Global rules, commit workflow, and the ORCHESTRATOR specification (plus the JSON template for new agents). |
| `.codex-swarm/agentctl.md` | 🧾 Quick reference for `python scripts/agentctl.py` commands + commit guardrails. |
| `.codex-swarm/swarm-config.json` | ⚙️ Framework config (paths for agents/docs/workflow/tasks). |
| `.codex-swarm/agents/PLANNER.json` | 🗒️ Defines how tasks are added/updated via `python scripts/agentctl.py` and kept aligned with each plan. |
| `.codex-swarm/agents/CODER.json` | 🔧 Implementation specialist responsible for code or config edits tied to task IDs. |
| `.codex-swarm/agents/TESTER.json` | 🧪 Adds or extends automated tests for the relevant code changes after implementation. |
| `.codex-swarm/agents/REVIEWER.json` | 👀 Performs reviews, runs `verify` commands, and finishes tasks via `python scripts/agentctl.py finish`. |
| `.codex-swarm/agents/DOCS.json` | 🧾 Writes per-task workflow artifacts under `docs/workflow/` and keeps docs synchronized. |
| `.codex-swarm/agents/CREATOR.json` | 🏗️ On-demand agent factory that writes new JSON agents plus registry updates. |
| `.codex-swarm/agents/UPDATER.json` | 🔍 Audits the repo and agent prompts when explicitly requested to outline concrete optimization opportunities and follow-up tasks. |
| `tasks.json` | 📊 Canonical backlog (checksum-backed). Do not edit by hand; use `python scripts/agentctl.py`. |
| `scripts/agentctl.py` | 🧰 Workflow helper for task ops (ready/start/block/task/verify/guard/finish) + tasks.json lint/checksum enforcement. |
| `README.md` | 📚 High-level overview and onboarding material for the repository. |
| `LICENSE` | 📝 MIT License for the project. |
| `assets/` | 🖼️ Contains the header image shown on this README and any future static visuals. |
| `clean.sh` | 🧹 Cleans the repository copy and restarts `git` so you can reuse the snapshot as your own local project. |
| `tasks.html` | 🖥️ A tiny local UI for browsing `tasks.json` in a browser (no server). |
| `docs/workflow/` | 🧾 Per-task workflow artifacts (one file per task ID). |

## 🧾 Commit Workflow

- The workspace is always a git repository, so every meaningful change must land in version control.
- Default to a minimal 3-phase commit cadence per task:
  - Planning: `tasks.json` + initial `docs/workflow/T-###.md` artifact.
  - Implementation: the actual change set (preferably including tests) as a single work commit.
  - Verification/closure: run checks, update `docs/workflow/T-###.md`, and mark the task `DONE` in `tasks.json`.
- The agent that performs the work stages and commits before handing control back to the orchestrator, briefly describing the completed plan item so the summary is obvious, and the orchestrator pauses the plan until that commit exists.
- Step summaries mention the new commit hash and confirm the working tree is clean so humans can audit progress directly from the conversation.
- If a plan step produces no file changes, call that out explicitly; otherwise the swarm must not proceed without a commit.
- Avoid extra commits that only move status fields (e.g., standalone “start/DOING” commits) unless truly necessary.

More background (concepts, diagrams, and “how it works”) lives in `docs/architecture.md`.
