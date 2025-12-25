# Framework Guideline

This document explains how to get the Codex Swarm framework ready and how to use it with the multi-agent workflow from AGENTS.md.

## 1. Overview

Codex Swarm is a local layering on top of the OpenAI Codex plugin. It keeps work predictable by making the Orchestrator plan in advance, the Planner manage the task backlog, and the specialists (CODER, DOCS, REVIEWER, etc.) execute their focused responsibilities. Every action is traceable through `.codex-swarm/tasks.json` and emoji-prefixed commits so collaborators know what happened, why, and who did it.

## 2. Prerequisites

- A git-savvy machine with Git installed (any recent version).
- Python 3.10+ for `.codex-swarm/agentctl.py` and any helper scripts.
- The OpenAI Codex plugin (Cursor, VS Code, JetBrains, or another supported editor) attached to this repository so the plugin can send files back and forth.
- Optional: a clean terminal (zsh/bash) that lets you run git, python, and shell scripts locally.

## 3. Initial setup

1. Clone the repository and `cd` into it:
   ```sh
   git clone https://github.com/basilisk-labs/codex-swarm.git
   cd codex-swarm
   ```
2. Open the project in your IDE with the Codex plugin enabled.
3. (Optional) Run `./clean.sh` if you want a clean slate; it removes framework-development artifacts and reinitializes git, leaving only the minimal files needed to reuse the framework as your own project.
4. Use `python .codex-swarm/agentctl.py task list` / `python .codex-swarm/agentctl.py task show T-123` to inspect tasks, and run `python .codex-swarm/agentctl.py task lint` after changes to keep `.codex-swarm/tasks.json` checksum-valid.
5. Keep `.codex-swarm/agents/*.json` open so you can see each agent’s permissions and workflow before you touch files.

## 4. Environment setup / “Installation” steps

1. Create or activate a Python virtual environment if you plan to install extra libraries for any scripts. For example:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install <needed-package>
   ```
   Always install dependencies inside the venv to avoid polluting the global site-packages.
2. Count `.codex-swarm/tasks.json` as the single source of truth for every task.
3. Keep `assets/` and `AGENTS.md` untouched unless your task explicitly calls for change.

## 5. Step-by-step usage flow

1. **Ask the Orchestrator for a goal.** Describe what you want to accomplish (e.g., “Document how to use the framework” or “Add a safety check”). The Orchestrator drafts a numbered plan with agents assigned to each step and waits for your approval before anything changes.
2. **PLANNER owns queue updates.** Once the plan is approved:
   - The PLANNER uses `python .codex-swarm/agentctl.py task add` / `python .codex-swarm/agentctl.py task update` to create or reprioritize tasks (no manual edits).
   - Run `python .codex-swarm/agentctl.py task lint` after task changes to keep the schema/deps/checksum valid.
3. **Workflow mode.** `.codex-swarm/config.json` controls `workflow_mode`:
   - `direct`: low-ceremony, single-checkout workflow (task branches/worktrees and PR artifacts are optional).
   - `branch_pr`: strict branching workflow (per-task branches/worktrees + tracked PR artifacts; `.codex-swarm/tasks.json` is single-writer and updated on `main` only).
4. **Specialist agents execute.** Work follows the JSON workflows:
   - *CODER* handles implementation, edits the relevant files, runs any commands (tests, linters), and documents the key command outputs.
   - *DOCS* updates documentation files (README, GUIDELINE.md, etc.) and ties each change back to the task ID.
   - *REVIEWER* reviews diffs and PR artifacts, and leaves short handoff notes in `.codex-swarm/workspace/T-123/pr/review.md` under `## Handoff Notes`.
   - *INTEGRATOR* is the only closer in `workflow_mode=branch_pr`: runs `pr check`, optionally `verify`, merges to `main`, then closes via `finish` (updates `.codex-swarm/tasks.json`).
5. **Committing.** Each task must end with a dedicated commit:
   - In `workflow_mode=branch_pr`, the implementation commit happens on the task branch (`task/T-123/<slug>`), and the closure commit happens on `main` (INTEGRATOR only).
   - Stage the relevant files and run `git commit -m "<emoji> T-<id> <short summary>"` (or use `python .codex-swarm/agentctl.py commit ...`).
   - Example: `git commit -m "📝 T-041 write framework guideline"`.
   - Mention the finished task ID and keep the message concise.
   - Before committing, validate the staged allowlist and message quality with `python .codex-swarm/agentctl.py guard commit T-123 -m "…" --allow <path>`.
   - In `branch_pr`, `finish` updates `.codex-swarm/tasks.json` (DONE + commit metadata + handoff notes), which must be committed on `main` with `--allow-tasks`.
6. **Final verification.** After the commit, `git status --short` must be clean. The agent who performed the task provides a summary referencing the files edited, commands run, and the new commit hash so the Orchestrator can track progress.
7. **Status sync.** Use `python .codex-swarm/agentctl.py task list` / `python .codex-swarm/agentctl.py task show T-123` to confirm the latest state (there is no separate status board file).

## 6. Common commands and expectations

- `.codex-swarm/agentctl.md`: Quick reference for the supported `agentctl` commands.
- `docs/architecture.md`: Pointer to the architecture/workflow section in `README.md` (concepts + Mermaid diagrams).
- `python .codex-swarm/agentctl.py agents`: List registered agents under `.codex-swarm/agents/`.
- `python .codex-swarm/agentctl.py task list` / `python .codex-swarm/agentctl.py task show T-123`: Inspect the backlog.
- `python .codex-swarm/agentctl.py task add/update/comment/set-status`: Modify tasks without breaking the checksum.
- `python .codex-swarm/agentctl.py ready/start/block/verify/finish`: Enforced task lifecycle with readiness + verify gates.
- `python .codex-swarm/agentctl.py task lint`: Validate schema/deps/checksum for `.codex-swarm/tasks.json`.
- `python .codex-swarm/agentctl.py guard clean/commit`: Git hygiene + staging allowlist checks.
- `python .codex-swarm/agentctl.py commit`: Optional wrapper that runs commit guards and then `git commit`.
- `./clean.sh`: Optional reset tool that removes framework-development artifacts and reinitializes git; use it when you want to reuse this repo as a fresh project.
- `git status --short`: Verify the tree is clean before handing control back.
- Use emoji-prefixed commit messages that mention the task ID.

## 7. Additional guidance

- Keep edits incremental and explain the “why” behind complex hunks with brief comments only when necessary.
- If work spans multiple agents (e.g., code + docs), make sure each agent’s workflow is respected and each associated task gets its own commit.
- Never run commands or edit files outside the repository unless the environment says otherwise; the default context is local-only.
- When in doubt about the workflow, consult `AGENTS.md` for the shared rules and `.codex-swarm/agents/<ID>.json` for the specific agent you need.

## 8. Example session

1. **State your goal to the Orchestrator.** The Orchestrator drafts a numbered plan, maps each step to the right agent (`PLANNER`, `CODER`, `DOCS`, etc.), and asks for your approval before anything mutates.
2. **PLANNER gates the backlog.** Once you approve, PLANNER adds/updates tasks via `python .codex-swarm/agentctl.py task add/update`, then runs `python .codex-swarm/agentctl.py task lint`.
3. **Specialists deliver the work.** CODER or DOCS run `python .codex-swarm/agentctl.py ready T-123`, start via `python .codex-swarm/agentctl.py start T-123 --author CODER --body "Start: …"`, then edit files and capture command output (tests, linters, scripts).
4. **Commit per task.** Stage the edited files, run `python .codex-swarm/agentctl.py guard commit T-123 -m "…" --allow <path>`, then commit with `git commit -m "<emoji> T-<id> <short summary>"`.
5. **Finish + cleanup (branch_pr).** INTEGRATOR (on clean `main`) runs `python .codex-swarm/agentctl.py pr check T-123`, then `python .codex-swarm/agentctl.py integrate T-123 --branch task/T-123/<slug> --run-verify`, and commits the resulting `.codex-swarm/tasks.json` change (plus docs updates) as the closure commit.

## 9. Troubleshooting & best practices

- `python .codex-swarm/agentctl.py task lint` fails with a checksum error: `.codex-swarm/tasks.json` was likely edited by hand. Undo the manual edit (e.g., `git checkout -- .codex-swarm/tasks.json`) and reapply the change via `python .codex-swarm/agentctl.py task update/comment/set-status` so the checksum stays valid.
- You’re looking at outdated task info: rerun `python .codex-swarm/agentctl.py task list` (or `task show T-123`) to confirm the latest state.
- Your working tree is dirty before committing: run `git status --short`, stash or revert unrelated changes, and keep future commits scoped to the current task.
- The Codex plugin stops responding: restart the IDE, reopen the repository, or re-execute your last command manually in a terminal before resuming.
- Need a clean slate? `./clean.sh` removes framework-development artifacts and reinitializes the repo so you can reuse the framework without carrying over the upstream history and docs.

By following these steps, you can install, use, and extend Codex Swarm predictably from your local IDE.
