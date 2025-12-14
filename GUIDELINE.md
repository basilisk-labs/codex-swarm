# Framework Guideline

This document explains how to get the Codex Swarm framework ready and how to use it with the multi-agent workflow from AGENTS.md.

## 1. Overview

Codex Swarm is a local layering on top of the OpenAI Codex plugin. It keeps work predictable by making the Orchestrator plan in advance, the Planner manage the task backlog, and the specialists (CODER, DOCS, REVIEWER, etc.) execute their focused responsibilities. Every action is traceable through `tasks.json` and emoji-prefixed commits so collaborators know what happened, why, and who did it.

## 2. Prerequisites

- A git-savvy machine with Git installed (any recent version).
- Python 3.10+ for `scripts/tasks.py` and any helper scripts.
- The OpenAI Codex plugin (Cursor, VS Code, JetBrains, or another supported editor) attached to this repository so the plugin can send files back and forth.
- Optional: a clean terminal (zsh/bash) that lets you run git, python, and shell scripts locally.

## 3. Initial setup

1. Clone the repository and `cd` into it:
   ```sh
   git clone https://github.com/basilisk-labs/codex-swarm.git
   cd codex-swarm
   ```
2. Open the project in your IDE with the Codex plugin enabled.
3. (Optional) Run `./clean.sh` if you want to remove the bundled assets, README copies, and git history before you begin; this script reinitializes the repository and gives you a blank slate.
4. Run `python scripts/tasks.py` whenever `tasks.json` changes to validate it and print a human-readable summary.
5. Keep `.AGENTS/*.json` open so you can see each agent’s permissions and workflow before you touch files.

## 4. Environment setup / “Installation” steps

1. Create or activate a Python virtual environment if you plan to install extra libraries for any scripts. For example:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install <needed-package>
   ```
   Always install dependencies inside the venv to avoid polluting the global site-packages.
2. Count `tasks.json` as the single source of truth for every task.
3. Keep `assets/` and `AGENTS.md` untouched unless your task explicitly calls for change.

## 5. Step-by-step usage flow

1. **Ask the Orchestrator for a goal.** Describe what you want to accomplish (e.g., “Document how to use the framework” or “Add a safety check”). The Orchestrator drafts a numbered plan with agents assigned to each step and waits for your approval before anything changes.
2. **PLANNER owns queue updates.** Once the plan is approved:
   - The PLANNER edits `tasks.json`, adds the new task (or tasks), and sets their `status` to `DOING` before work begins.
   - After editing `tasks.json`, run `python scripts/tasks.py` to validate and review a readable summary.
3. **Specialist agents execute.** Work follows the JSON workflows:
   - *CODER* handles implementation, edits the relevant files, runs any commands (tests, linters), and documents the key command outputs.
   - *DOCS* updates documentation files (README, GUIDELINE.md, etc.) and ties each change back to the task ID.
   - *REVIEWER* inspects diffs, reruns commands if needed, and marks the task `DONE` in `tasks.json` once the work passes review. Every status update should be followed by `python scripts/tasks.py` to validate and confirm the latest state.
4. **Committing.** Each task must end with a dedicated commit:
   - Stage the relevant files and run `git commit -m "<emoji> T-<id> <short summary>"`.
   - Example: `git commit -m "📝 T-041 write framework guideline"`.
   - Mention the finished task ID and keep the message concise.
5. **Final verification.** After the commit, `git status --short` must be clean. The agent who performed the task provides a summary referencing the files edited, commands run, and the new commit hash so the Orchestrator can track progress.
6. **Status sync.** After status changes, rerun `python scripts/tasks.py` to validate `tasks.json` and confirm the latest state.

## 6. Common commands and expectations

- `python scripts/tasks.py`: Validates `tasks.json`, syncs commit metadata, and prints a human-readable summary. Run this after changes to the JSON file (additions, status flips, comments, etc.).
- `./clean.sh`: Optional reset tool that deletes the bundled assets and reinitializes the git history; use it when you want to reuse this repo as a fresh project.
- `git status --short`: Verify the tree is clean before handing control back.
- Use emoji-prefixed commit messages that mention the task ID.

## 7. Additional guidance

- Keep edits incremental and explain the “why” behind complex hunks with brief comments only when necessary.
- If work spans multiple agents (e.g., code + docs), make sure each agent’s workflow is respected and each associated task gets its own commit.
- Never run commands or edit files outside the repository unless the environment says otherwise; the default context is local-only.
- When in doubt about the workflow, consult `AGENTS.md` for the shared rules and `.AGENTS/<ID>.json` for the specific agent you need.

## 8. Example session

1. **State your goal to the Orchestrator.** The Orchestrator drafts a numbered plan, maps each step to the right agent (`PLANNER`, `CODER`, `DOCS`, etc.), and asks for your approval before anything mutates.
2. **PLANNER gates the backlog.** Once you approve, PLANNER edits `tasks.json`, adds the task with `status: DOING`, and runs `python scripts/tasks.py` to validate and review the latest state.
3. **Specialists deliver the work.** CODER or DOCS edit files, capture command output (tests, linters, or scripts), and keep every change focused on the assigned files. REVIEWER double-checks the diff, reruns commands if needed, and flips the task to `DONE`.
4. **Commit per task.** Stage the edited files and `git commit -m "<emoji> T-<id> <short summary>"`—the message should mention the task ID so `scripts/tasks.py` can automatically link the commit back to the ticket.
5. **Cleanup.** Run `git status --short` to ensure the tree is clean, rerun `python scripts/tasks.py` to validate `tasks.json`, and let the Orchestrator know about the new commit hash so the plan can continue.

## 9. Troubleshooting & best practices

- `python scripts/tasks.py` crashes with a JSON error: the file was likely malformed. Open `tasks.json`, fix the highlighted entry (commas, quotes, or missing braces), then rerun the script. Use `rg -n '"T-042' tasks.json` to locate the entry quickly.
- You’re looking at outdated task info: rerun `python scripts/tasks.py` (or reopen `tasks.json`) to confirm the latest state.
- Your working tree is dirty before committing: run `git status --short`, stash or revert unrelated changes, and keep future commits scoped to the current task.
- The Codex plugin stops responding: restart the IDE, reopen the repository, or re-execute your last command manually in a terminal before resuming.
- Need a clean slate? `./clean.sh` removes the bundled docs and git history, then reinitializes the repo so you can reuse the framework without carrying over artifacts.

By following these steps, you can install, use, and extend Codex Swarm predictably from your local IDE.
