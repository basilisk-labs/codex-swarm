# Codex Agents Swarm

Codex Agents Swarm is a lightweight framework that bridges the OpenAI Codex Plugin with any IDE where the plugin is installed. It treats the IDE session as a cooperative multi-agent workspace, allowing you to orchestrate specialized agents that collaborate on tasks ranging from software development to documentation, planning, or research.

## How It Works

1. **Orchestrator-focused contract.** `AGENTS.md` defines only the global rules, shared state, and the ORCHESTRATOR agent. The orchestrator interprets the user’s goal, drafts a plan, requests approval, and delegates work to other agents.
2. **External agent registry.** Every non-orchestrator agent lives in `.AGENTS/<ID>.json`. When the IDE loads this repository, it dynamically imports each JSON document and registers the agent ID, role, permissions, and workflow.
3. **Shared task state.** All task data lives in the root-level `tasks.json`, and `scripts/tasks.py` regenerates a human-readable `tasks.md` so everyone can scan the backlog without editing JSON.
4. **Plugin-agnostic operation.** Because the instructions are plain Markdown and JSON, any IDE that supports the Codex Plugin can execute the same flows without extra configuration.

## Repository Layout

```
.
├── AGENTS.md
├── LICENSE
├── README.md
├── tasks.json
├── tasks.md
├── scripts
│   └── tasks.py
└── .AGENTS/
    ├── PLANNER.json
    ├── CODER.json
    ├── REVIEWER.json
    ├── DOCS.json
    └── CREATOR.json
```

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Global rules, commit workflow, and the ORCHESTRATOR specification (plus the JSON template for new agents). |
| `.AGENTS/PLANNER.json` | Defines how tasks are added/updated inside `tasks.json` and regenerated into `tasks.md`. |
| `.AGENTS/CODER.json` | Implementation specialist responsible for code or config edits tied to task IDs. |
| `.AGENTS/REVIEWER.json` | Performs reviews, verifies work, and flips task statuses accordingly. |
| `.AGENTS/DOCS.json` | Keeps README and other docs synchronized with recently completed work. |
| `.AGENTS/CREATOR.json` | On-demand agent factory that writes new JSON agents plus registry updates. |
| `tasks.json` | Canonical backlog with status, priority, description, tags, and threaded comments. |
| `tasks.md` | Generated human-readable board grouped by status buckets (do not edit by hand). |
| `scripts/tasks.py` | Utility script that reads `tasks.json` and rewrites `tasks.md` so both stay in sync. |
| `README.md` | High-level overview and onboarding material for the repository. |
| `LICENSE` | MIT License for the project. |

## Agent Lifecycle

1. **Planning:** The ORCHESTRATOR reads `AGENTS.md`, loads `.AGENTS/*.json`, and creates a plan that maps each step to a registered agent (e.g., PLANNER, CODER, REVIEWER, DOCS).
2. **Approval:** The user can approve, edit, or cancel the plan before any work starts.
3. **Execution:** The orchestrator switches `agent_mode` according to the plan, allowing each agent to follow its JSON-defined workflow inside the IDE.
4. **Progress tracking:** Agents edit `tasks.json` according to their permissions and rerun `python scripts/tasks.py` so `tasks.md` instantly reflects the new state.

This structure lets you string together arbitrary workflows such as code implementation, documentation refreshes, research digests, or task triage—all from the same IDE session.

## Commit Workflow

- The workspace is always a git repository, so every meaningful change must land in version control.
- Each atomic task listed in `tasks.json` maps to exactly one commit with a concise, meaningful emoji-prefixed message (ideally referencing the task ID).
- The agent that performs the work stages and commits before handing control back to the orchestrator, briefly describing the completed plan item so the summary is obvious, and the orchestrator pauses the plan until that commit exists.
- Step summaries mention the new commit hash and confirm the working tree is clean so humans can audit progress directly from the conversation.
- If a plan step produces no file changes, call that out explicitly; otherwise the swarm must not proceed without a commit.

## Shared State Details

- **`tasks.json`**: Canonical backlog file containing every task’s ID, title, description, status, priority, owner, tags, and threaded comments. Agents edit this file directly (usually via PLANNER/REVIEWER) so automation always has reliable state.
- **`tasks.md`**: Generated dashboard created by running `python scripts/tasks.py`. It groups tasks into Backlog / In Progress / Blocked / Done, shows metadata, and mirrors the latest `comments` snippets so humans can skim progress without opening the JSON.
- **`scripts/tasks.py`**: Small CLI helper that reads `tasks.json` and rewrites `tasks.md`. Run it every time task data changes; do not edit `tasks.md` manually.

## Adding a New Agent

1. Duplicate the template defined in `AGENTS.md` under “JSON Template for New Agents”.
2. Save the file as `.AGENTS/<AGENT_ID>.json` using an uppercase ID (e.g., `RESEARCHER.json`).
3. Fill in the `role`, `description`, `inputs`, `outputs`, `permissions`, and ordered `workflow` steps that describe exactly how the agent should behave.
4. Commit the file; on the next run the orchestrator will automatically load and expose the new agent.

Because every agent is pure JSON, you can extend the swarm with domain experts for QA, marketing, technical writing, data wrangling, or any other process you want to automate in your IDE.

## Extending Beyond Development

While Codex Agents Swarm is comfortable implementing code, nothing restricts agents to development tasks. By defining workflows in JSON you can build:

- Research agents that summarize documentation before coding begins.
- Compliance reviewers that check commits for policy violations.
- Operational runbooks that coordinate deployments or incident response.
- Documentation bots that keep changelogs and READMEs in sync.

If the OpenAI Codex Plugin can access the repository from your IDE, it can orchestrate these agents using the same framework.
