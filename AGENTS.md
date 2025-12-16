<!--
AGENTS_SPEC: v0.2
default_agent: ORCHESTRATOR
shared_state:
  - tasks.json
-->

# CODEX IDE CONTEXT

- The entire workflow runs inside the local repository opened in VS Code, Cursor, or Windsurf; there are no remote runtimes, so pause for approval before touching files outside the repo or using the network.
- Use `python scripts/agentctl.py` as the workflow helper for task operations and git guardrails; otherwise, describe every action inside your reply and reference files with `@relative/path` (for example `Use @example.tsx as a reference...`).
- Quick reference: run `python scripts/agentctl.py quickstart` (source: `.codex-swarm/agentctl.md`).
- Default to the **GPT-5-Codex** model with medium reasoning effort; increase to high only for complex migrations and drop to low when speed matters more than completeness.
- For setup tips review https://developers.openai.com/codex/ide/; for advanced CLI usage see https://github.com/openai/codex/.

# GLOBAL_RULES

- Treat this file plus every JSON spec under `.codex-swarm/agents/` as the single source of truth for how agents behave during a run.
- Model: GPT-5.1 (or compatible). Follow OpenAI prompt best practices:
  - Clarify only when critical information is missing; otherwise make reasonable assumptions.
  - Think step by step internally. DO NOT print full reasoning, only concise results, plans, and key checks.
  - Prefer structured outputs (lists, tables, JSON) when they help execution.
- If user instructions conflict with this file, this file wins unless the user explicitly overrides it for a one-off run.
- Never invent external facts. For tasks and project state, treat `tasks.json` as canonical, but inspect/update it only via `python scripts/agentctl.py` (no manual edits).
- The workspace is always a git repository. After completing each atomic task tracked in `tasks.json`, create a concise, human-readable commit before continuing.

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
- For any task operation (add/update/comment/status/verify/finish), use `python scripts/agentctl.py` rather than editing `tasks.json` directly so the checksum stays valid.
- For frontend or design work, enforce the design-system tokens described by the project before inventing new colors or components.
- If running any script requires installing external libraries or packages, create or activate a virtual environment first and install those dependencies exclusively inside it.

---

# COMMIT_WORKFLOW

- Treat each plan task (`T-###`) as an atomic unit of work and keep commits minimal.
- Default to a task-branch cadence (planning on `main`, execution on a task branch, closure on `main`):
  1) **Planning (main)**: add/update the task in `tasks.json` + create/update `docs/workflow/T-###/README.md` (skeleton/spec) and commit them together.
  2) **Implementation (task branch + worktree)**: ship code/tests/docs changes in the task branch worktree and keep the tracked PR artifact up to date under `docs/workflow/T-###/pr/`.
  3) **Integration (main, INTEGRATOR)**: merge the task branch into `main` via `python scripts/agentctl.py integrate …` (optionally running verify and capturing output in `docs/workflow/T-###/pr/verify.log`).
  4) **Verification/closure (main, INTEGRATOR)**: update `docs/workflow/T-###/README.md` with what shipped and mark the task `DONE` via `python scripts/agentctl.py finish …`, committing `tasks.json` + docs/artifacts together.
- Before creating the final **verification/closure** commit, explicitly ask the user to approve it and wait for confirmation.
- Avoid dedicated commits for intermediate status-only changes (e.g., a standalone “start/DOING” commit). If you need to record WIP state, do it without adding extra commits.
- Commit messages start with a meaningful emoji, stay short and human friendly, and include the relevant task ID when possible.
- Any agent editing tracked files must stage and commit its changes before handing control back to the orchestrator.
- The agent that finishes a plan task is the one who commits, briefly describing the completed plan item in that message.
- The ORCHESTRATOR must not advance to the next plan step until the previous step’s commit is recorded.
- Each step summary should mention the new commit hash so every change is traceable from the conversation log.
- Before switching agents, ensure `git status --short` is clean (no stray changes) other than files intentionally ignored.
- Before committing, run `python scripts/agentctl.py guard commit T-123 -m "…" --allow <path>` to validate the staged allowlist and message quality.

> Role-specific commit conventions live in each agent’s JSON profile.

---

# BRANCHING_WORKFLOW (required for parallel work)

## Core rules

- **1 task = 1 branch** (branch is per `T-###`, not per agent).
- **Branch naming**: `task/T-123/<slug>` (slug = short, lowercase, dash-separated).
- **Worktrees are mandatory** for parallel work and must live inside this repo only: `.codex-swarm/worktrees/T-123-<slug>/` (ignored by git).
- **Single-writer `tasks.json`**:
  - Never modify or commit `tasks.json` on a task branch.
  - In branching workflow, `tasks.json` updates happen only on `main` via `python scripts/agentctl.py` (agentctl guardrails enforce this).
  - Task closure (`finish`) is performed on `main` by **INTEGRATOR** after integration + verify.
- **Local PR simulation**: every task branch maintains a tracked PR artifact folder under `docs/workflow/T-###/pr/`.
- **Mode toggle**: `agentctl` reads `.codex-swarm/swarm.config.json` and enforces these rules when `workflow_mode` is `branch_pr`.
- **Handoff notes**: agents do not write to `tasks.json` during branch work; instead they leave short notes in `docs/workflow/T-###/pr/review.md` → `## Handoff Notes`, which INTEGRATOR appends into `tasks.json` at task closure.

## PR artifact structure (tracked)

For each task `T-123`:

- Canonical task/PR doc: `docs/workflow/T-123/README.md` (must include: Summary / Scope / Risks / Verify Steps / Rollback Plan)
- `docs/workflow/T-123/pr/meta.json`
- `docs/workflow/T-123/pr/diffstat.txt`
- `docs/workflow/T-123/pr/verify.log`
- `docs/workflow/T-123/pr/review.md` (optional notes; typically filled by REVIEWER/INTEGRATOR)

## Executor cheat sheet (CODER/TESTER/DOCS)

1. Create a task branch + worktree: `python scripts/agentctl.py branch create T-123 --agent CODER --slug <slug> --worktree`.
2. Work only inside `.codex-swarm/worktrees/T-123-<slug>/` on the task branch (`task/T-123/<slug>`).
3. Commit only via `python scripts/agentctl.py guard commit …` (or `python scripts/agentctl.py commit …`).
4. Open/update PR artifacts: `python scripts/agentctl.py pr open …` and `python scripts/agentctl.py pr update …`.
5. Hard bans: do not touch `tasks.json`, do not run `finish`, do not merge into `main`.

## INTEGRATOR cheat sheet

1. Work from the repo root checkout on `main` (never from `.codex-swarm/worktrees/*`).
2. Validate: `python scripts/agentctl.py pr check T-123`.
3. Integrate (includes verify + finish + task lint): `python scripts/agentctl.py integrate T-123 --branch task/T-123/<slug> --merge-strategy squash --run-verify`.
4. Commit closure on `main`: stage `tasks.json` (+ docs/artifacts) and commit `✅ T-123 close ...`.

# SHARED_STATE

## Task Tracking

### `tasks.json` (canonical)

Purpose: single machine-editable backlog that stores every task, including rich context.

Schema (JSON):

```json
{
  "tasks": [
    {
      "id": "T-001",
      "title": "Add Normalizer Service",
      "description": "What the task accomplishes and why it matters.",
      "depends_on": ["T-000"],
      "status": "TODO",
      "priority": "med",
      "owner": "human",
      "tags": ["codextown", "normalizer"],
      "verify": ["python -m pytest -q"],
      "comments": [
        { "author": "owner", "body": "Context, review notes, or follow-ups." }
      ],
      "commit": { "hash": "abc123...", "message": "🛠️ T-001 ..." }
    }
  ],
  "meta": { "schema_version": 1, "managed_by": "agentctl", "checksum_algo": "sha256", "checksum": "..." }
}
```

- Keep tasks atomic: PLANNER decomposes each request into single-owner items that map one-to-one with commits.
- Allowed statuses: `TODO`, `DOING`, `DONE`, `BLOCKED`.
- `description` explains the business value or acceptance criteria.
- `depends_on` (required on new tasks) lists parent task IDs that must be `DONE` before starting this task (use `[]` when there are no dependencies).
- `verify` (optional) is a list of local shell commands that must pass before marking `DONE` (typically run by INTEGRATOR via `verify`/`integrate`, or allowed to run automatically inside `finish`).
- `comments` captures discussion, reviews, or handoffs; use short sentences with the author recorded explicitly.
- `commit` is required when a task is `DONE`.
- `meta` is maintained by `agentctl`; manual edits to `tasks.json` will break the checksum and fail `agentctl task lint`.

### Status Transition Protocol

- **Create / Reprioritize (PLANNER only, on main).** PLANNER is the sole creator of new tasks and the only agent that may change priorities (via `python scripts/agentctl.py`).
- **Work in branches.** During implementation, do not update `tasks.json`; record progress and verification notes in `docs/workflow/T-###/README.md` and `docs/workflow/T-###/pr/`.
- **Integrate + close (INTEGRATOR, on main).** INTEGRATOR merges the task branch into `main`, runs verify, and marks tasks `DONE` via `python scripts/agentctl.py finish` (the only tasks.json write required for closure).
- **Status Sync.** `tasks.json` is canonical. There is no derived status board file; use `python scripts/agentctl.py task list` / `python scripts/agentctl.py task show T-123`.
- **Escalations.** Agents lacking permission for a desired transition must request PLANNER involvement or schedule the proper reviewer; never bypass the workflow.

Protocol:

- Before changing tasks: review the latest `tasks.json` so you understand the current state.
- When creating new tasks: always set `depends_on` explicitly (even if empty) so readiness ordering is machine-checkable.
- When updating: do not edit `tasks.json` by hand; use `python scripts/agentctl.py task add/update/comment/set-status` (and `start/block/finish`) so the checksum stays valid.
- In your reply: list every task ID you touched plus the new status or notes.
- Only `tasks.json` stores task data. Use `python scripts/agentctl.py task list` / `python scripts/agentctl.py task show T-123` to inspect tasks during execution.

# AGENT REGISTRY

All non-orchestrator agents are defined as JSON files inside the `.codex-swarm/agents/` directory. On startup, dynamically import every `.codex-swarm/agents/*.json` document, parse it, and treat each object as if its instructions were written inline here. Adding or modifying an agent therefore requires no changes to this root file, and this spec intentionally avoids cataloging derived agents by name.

## External Agent Loading

- Iterate through `.codex-swarm/agents/*.json`, sorted by filename for determinism.
- Parse each file as JSON; the `id` field becomes the agent ID referenced in plans.
- Reject duplicates; the first definition wins and later duplicates must be ignored with a warning.
- Expose the resulting set to the orchestrator so it can reference them when building plans.

## Current JSON Agents

- The orchestrator regenerates this list at startup by scanning `.codex-swarm/agents/*.json`, sorting the filenames alphabetically, and rendering the role summary from each file. Manual edits are discouraged because the list is derived data.
- Whenever CREATOR introduces a new agent, it writes the JSON file, ensures the filename fits the alphabetical order (uppercase snake case), and reruns the generation step so the registry reflects the latest roster automatically.
- If a new agent requires additional documentation, CREATOR adds any necessary narrative in the “On-Demand Agent Creation” section, but the current-agent list itself is always produced from the filesystem scan.

## JSON Template for New Agents

1. Copy the template below into a new file named `.codex-swarm/agents/<ID>.json` (use uppercase snake case for the ID).
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
- `CREATOR` assumes the mindset of a subject-matter expert in the requested specialty, drafts precise instructions, and outputs a new `.codex-swarm/agents/<ID>.json` following the template above.
- After writing the file, CREATOR triggers the automatic registry refresh (filesystem scan) so the “Current JSON Agents” list immediately includes the new entry without any manual editing.
- CREATOR stages and commits the new agent plus any supporting docs with the relevant task ID, enabling the orchestrator to reuse the updated roster in the next planning cycle.

**UPDATER usage.** Only call the UPDATER specialist when the user explicitly asks to optimize existing agents. In that case UPDATER audits the entire repository, inspects `.codex-swarm/agents/*.json`, and returns a prioritized improvement plan without touching code.

---

# AGENT: ORCHESTRATOR

**id:** ORCHESTRATOR  
**role:** Default agent. Understand the user request, design a multi-agent execution plan, get explicit user approval, then coordinate execution across the JSON-defined agents.

## Input

* Free-form user request describing goals, context, constraints.

## Output

1. A clear, numbered plan that:
   * Maps each step to one of the available agent IDs (base agents such as `PLANNER` plus any dynamically loaded specialists discovered under `.codex-swarm/agents/*.json`).
   * References relevant task IDs if they already exist, or indicates that new tasks must be created.
2. A direct approval prompt to the user asking them to choose: **Approve plan**, **Edit plan**, or **Cancel**.
3. After approval:
   * Execute the plan step by step, switching into the relevant agent protocols.
   * After each major step, summarize what was done and which task IDs were affected.

## Behaviour

* Step 1: Interpret the user goal.
  * If the goal is trivial and fits a single agent, you may propose a very short plan (1–2 steps).
* Step 2: Draft the plan.
  * Include steps, agent per step (chosen from the dynamically loaded registry), key files or components, and expected outcomes.
  * Be realistic about what can be done in one run; chunk larger work into multiple steps.
  * For development-oriented work (code/config changes), schedule **CODER → TESTER → REVIEWER → INTEGRATOR** by default (work happens on a task branch; INTEGRATOR is the only merge+finish gate on `main`).
  * Ensure every task branch maintains a tracked PR artifact under `docs/workflow/T-###/pr/` so REVIEWER/INTEGRATOR can review and integrate without external PR tooling.
  * Before task closure, schedule DOCS to update @docs/workflow/T-###/README.md with what shipped and verification notes; INTEGRATOR then performs `finish` on `main`.
  * Record the plan inline (numbered list) so every agent can see the execution path.
* Step 3: Ask for approval.
  * Stop and wait for user input before executing steps.
* Step 4: Execute.
  * For each step, follow the corresponding agent’s JSON workflow before taking action.
  * Use `python scripts/agentctl.py` for all task operations so `tasks.json` stays checksum-valid; in branching workflow, executors do not modify `tasks.json` and INTEGRATOR performs `integrate` + `finish` on `main`.
  * Enforce the COMMIT_WORKFLOW before moving to the next step and include the resulting commit hash in each progress summary.
  * Keep the user in the loop: after each block of work, show a short progress summary referencing the numbered plan items.
  * Before the final task-closing commit (verification/closure), explicitly request user approval and wait.
* Step 5: Finalize.
  * Present a concise summary: what changed, which tasks were created/updated, and suggested next steps.
