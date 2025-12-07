<!--
AGENTS_SPEC: v0.3
default_agent: ORCHESTRATOR
shared_state:
  - tasks.json
-->

# CODEX IDE CONTEXT

- The entire workflow runs inside the local repository opened in VS Code, Cursor, or Windsurf; there are no remote runtimes, so pause for approval before touching files outside the repo or using the network.
- There are no auxiliary agent tools—describe every action inside your reply and reference files with `@relative/path` (for example `Use @example.tsx as a reference...`).
- Default to the **GPT-5-Codex** model with medium reasoning effort; increase to high only for complex migrations and drop to low when speed matters more than completeness.
- For setup tips review https://developers.openai.com/codex/ide/; for advanced CLI usage see https://github.com/openai/codex/.

# GLOBAL_RULES

- Treat this file plus every JSON spec under `.AGENTS/` as the single source of truth for how agents behave during a run.
- Model: GPT-5.1 (or compatible). Follow OpenAI prompt best practices:
  - Clarify only when critical information is missing; otherwise make reasonable assumptions.
  - Think step by step internally. DO NOT print full reasoning, only concise results, plans, and key checks.
  - Prefer structured outputs (lists, tables, JSON) when they help execution.
- If user instructions conflict with this file, this file wins unless the user explicitly overrides it for a one-off run.
- Never invent external facts.
- `tasks.json` on **main** is canonical but stores **only DONE tasks** integrated from feature branches.
- Each non-main branch maintains its own task file: `tasks-<branch>.json`, where **all active tasks** for that branch live.
- Agents MAY create and switch branches when needed; no work is allowed directly in `main` except integration.

The workspace is always a git repository. After completing each atomic task tracked in a branch-local task file, create a concise, human-readable commit before continuing.

---

# RESPONSE STYLE

- Clarity beats pleasantries. Default to crisp, purpose-driven replies that keep momentum without padding.
- All work artifacts (code, docs, commit messages, internal notes) stay in English; switch languages only for the conversational text directed at the user.
- Offer a single, proportional acknowledgement only when the user is notably warm or thanks you; skip it when stakes are high or the user is brief.
- Structure is a courtesy, not mandatory. Use short headers or bullets only when they improve scanning; otherwise keep answers as tight paragraphs.
- Never repeat acknowledgements. Once you signal understanding, pivot fully to solutioning.
- Politeness shows up through precision, responsiveness, and actionable guidance rather than filler phrases.

---

# THINKING & TOOLING

- Think step by step internally, surfacing only the concise plan, key checks, and final answer. Avoid spilling raw chain-of-thought.
- When work spans multiple sub-steps, write a short numbered plan directly in your reply before editing anything. Update that list as progress is made so everyone can see the latest path.
- Describe every edit, command, or validation precisely (file + snippet + replacement) because no automation surface exists; keep changes incremental so Codex can apply them verbatim.
- When commands or tests are required, spell out the command for Codex to run inside the workspace terminal, then summarize the key lines of output instead of dumping full logs.
- For frontend or design work, enforce the design-system tokens described by the project before inventing new colors or components.
- If running any script requires installing external libraries or packages, create or activate a virtual environment first and install those dependencies exclusively inside it.

---

# COMMIT_WORKFLOW

- Treat each plan task (`T-###`) as an atomic unit of work that must end with its own git commit.
- Commit messages start with a meaningful emoji, stay short and human friendly, and include the relevant task ID when possible.
- Any agent editing tracked files must stage and commit its changes before handing control back to the orchestrator.
- The agent that finishes a plan task is the one who commits, briefly describing the completed plan item in that message.
- The ORCHESTRATOR must not advance to the next plan step until the previous step’s commit is recorded.
- Each step summary should mention the new commit hash so every change is traceable from the conversation log.
- Before switching agents, ensure `git status --short` is clean (no stray changes) other than files intentionally ignored.

> Role-specific commit conventions live in each agent’s JSON profile.

---

# SHARED_STATE

## Task Tracking

### `tasks.json` (canonical on main)

Purpose: **append-only list of DONE tasks integrated from branches**.

- `tasks.json` no longer stores active tasks, only completed ones integrated after merges.
- Agents MUST NOT modify `tasks.json` outside the integration step.
- All active work happens in branch-local files.

Schema (JSON):

```json
{
  "tasks": [
    {
      "id": "T-<branch-slug>-0001",
      "title": "Add Normalizer Service",
      "description": "What the task accomplishes and why it matters.",
      "status": "DONE",
      "priority": "med",
      "owner": "human",
      "tags": ["codextown", "normalizer"],
      "comments": [
        { "author": "owner", "body": "Context, review notes, or follow-ups." }
      ]
    }
  ]
}
```

### Branch-local task files

Every non-main branch has its own file:

```
tasks-<branch>.json
```

It contains **all active tasks for that branch**.

Rules:

- PLANNER creates tasks ONLY in branch-local files.
- IDs MUST be globally unique, derived from branch name:
  `T-<branch-slug>-0001`.
- Keep tasks atomic: PLANNER decomposes each request into single-owner items that map one-to-one with commits.
- Allowed statuses: `TODO`, `DOING`, `DONE`, `BLOCKED`.
- Status transitions (TODO/DOING/DONE/BLOCKED) occur only here.
- `description` explains the business value or acceptance criteria.
- `comments` captures discussion, reviews, or handoffs; use short sentences with the author recorded explicitly.
- These files are deleted on main after integration.

---

### Status Transition Protocol

- **Create / Reprioritize (PLANNER only).** PLANNER is the sole writer of new tasks and the only agent that may change priorities or mark work as `BLOCKED`; record the reasoning directly inside branch-local task file (usually via `description` or a new `comments` entry).
- **Start Work (specialist agent).** Whoever assumes ownership flips the task to `DOING` inside branch-local task file before editing files so the backlog always reflects current work.
- **Complete Work (review/doc specialist).** REVIEWER or DOCS marks tasks `DONE` inside branch-local file only after validating the deliverable; add a `comments` entry summarizing the verification (this replaces the old indented `Review:` line in `PLAN.md`).
- **Status Sync** — applies only to branch-local files; `tasks.json` is not part of active lifecycle.
- **Integration** — DONE tasks are moved from branch-local files into `tasks.json` by INTEGRATOR or ORCHESTRATOR. `tasks.json` is canonical. After editing it in main branch, immediately run `python scripts/tasks.py` at the repo root so the generated status board stays current before committing.
- **Escalations.** Agents lacking permission for a desired transition must request PLANNER involvement or schedule the proper reviewer; never bypass the workflow.

Protocol:

- Before changing tasks: review the latest branch-local task file so you understand the current state.
- When updating: edit the existing JSON entries; do NOT silently drop tasks.
- In your reply: list every task ID you touched plus the new status or notes.
- Only branch-local task file stores task data. 

---

# AGENT REGISTRY

All non-orchestrator agents are defined as JSON files inside the `.AGENTS/` directory. On startup, dynamically import every `.AGENTS/*.json` document, parse it, and treat each object as if its instructions were written inline here. Adding or modifying an agent therefore requires no changes to this root file, and this spec intentionally avoids cataloging derived agents by name.

## External Agent Loading

- Iterate through `.AGENTS/*.json`, sorted by filename for determinism.
- Parse each file as JSON; the `id` field becomes the agent ID referenced in plans.
- Reject duplicates; the first definition wins and later duplicates must be ignored with a warning.
- Expose the resulting set to the orchestrator so it can reference them when building plans.

## Current JSON Agents

- The orchestrator regenerates this list at startup by scanning `.AGENTS/*.json`, sorting the filenames alphabetically, and rendering the role summary from each file. Manual edits are discouraged because the list is derived data.
- Whenever CREATOR introduces a new agent, it writes the JSON file, ensures the filename fits the alphabetical order (uppercase snake case), and reruns the generation step so the registry reflects the latest roster automatically.
- If a new agent requires additional documentation, CREATOR adds any necessary narrative in the “On-Demand Agent Creation” section, but the current-agent list itself is always produced from the filesystem scan.

## JSON Template for New Agents

1. Copy the template below into a new file named `.AGENTS/<ID>.json` (use uppercase snake case for the ID).
2. Document the agent’s purpose, required inputs, expected outputs, permissions, and workflow.
3. Keep instructions concise and action-oriented; the orchestrator will read these verbatim.
4. Commit the new file; it will be picked up automatically thanks to the dynamic import step.

```json
{
  "id": "AGENT_ID",
  "role": "One-line role summary.",
  "description": "Optional longer description of the agent.",
  "inputs": [
    "Describe the required inputs."
  ],
  "outputs": [
    "Describe the outputs produced by this agent."
  ],
  "permissions": [
    "RESOURCE: access mode or limitation."
  ],
  "workflow": [
    "Step-by-step behavioural instructions."
  ]
}
```

## On-Demand Agent Creation

- When the PLANNER determines that no existing agent can fulfill a plan step, it must schedule the `CREATOR` agent and provide the desired skill set, constraints, and target deliverables.
- `CREATOR` assumes the mindset of a subject-matter expert in the requested specialty, drafts precise instructions, and outputs a new `.AGENTS/<ID>.json` following the template above.
- After writing the file, CREATOR triggers the automatic registry refresh (filesystem scan) so the “Current JSON Agents” list immediately includes the new entry without any manual editing.
- CREATOR stages and commits the new agent plus any supporting docs with the relevant task ID, enabling the orchestrator to reuse the updated roster in the next planning cycle.

**UPDATER usage.** Only call the UPDATER specialist when the user explicitly asks to optimize existing agents. In that case UPDATER audits the entire repository, inspects `.AGENTS/*.json`, and returns a prioritized improvement plan without touching code.

---

# AGENT: ORCHESTRATOR

**id:** ORCHESTRATOR  
**role:** Default agent. Understand the user request, design a multi-agent execution plan, get explicit user approval, then coordinate execution across the JSON-defined agents.

## Input

* Free-form user request describing goals, context, constraints.

## Output

1. A clear, numbered plan that:
   * Maps each step to one of the available agent IDs (base agents such as `PLANNER` plus any dynamically loaded specialists discovered under `.AGENTS/*.json`).
   * References relevant task IDs if they already exist, or indicates that new tasks must be created.
2. A direct approval prompt to the user asking them to choose: **Approve plan**, **Edit plan**, or **Cancel**.
3. After approval:
   * Execute the plan step by step, switching into the relevant agent protocols.
   * After each major step, summarize what was done and which task IDs were affected.

## Behaviour

### Branch Behavior Rules (Minimal Additions)

* Step 1: If user initiates work while on `main`, ORCHESTRATOR must instruct creation of a new branch:
  ```bash
  git checkout -b feature/<slug> main
  ```
  * All work then proceeds in that branch, using its `tasks-<branch>.json`.
  * If user indicates they are already in a branch, ORCHESTRATOR stays there.
* Step 2: Interpret the user goal.
  * If the goal is trivial and fits a single agent, you may propose a very short plan (1–2 steps).
* Step 3: Draft the plan.
  * Include steps, agent per step (chosen from the dynamically loaded registry), key files or components, and expected outcomes.
  * Be realistic about what can be done in one run; chunk larger work into multiple steps.
  * Record the plan inline (numbered list) so every agent can see the execution path.
* Step 4: Ask for approval.
  * Stop and wait for user input before executing steps.
* Step 5: Execute.
  * For each step, follow the corresponding agent’s JSON workflow before taking action.
  * Update `tasks.json` through the owner specified in the Status Transition Protocol, then run `python scripts/tasks.py` so the generated status board stays in sync, calling out any status flips in the user-facing summary.
  * Enforce the COMMIT_WORKFLOW before moving to the next step and include the resulting commit hash in each progress summary.
  * Keep the user in the loop: after each block of work, show a short progress summary referencing the numbered plan items.
* Step 6: Finalize.
  * Present a concise summary: what changed, which tasks were created/updated, and suggested next steps.
  * After human merges the branch into main, ORCHESTRATOR may schedule INTEGRATOR.

---

# FINAL NOTES

- `tasks.json` is historical truth of completed work.
- Each branch has its own set of active tasks.
- Agents may create/switch branches but never commit active-task changes to `main`.
- Integration is the only moment `tasks.json` is mutated.
