# agentctl quickstart

`python .codex-swarm/agentctl.py` is the only supported way to inspect/update `.codex-swarm/tasks.json` (manual edits break the checksum).

## Agent management source of truth

This file is the canonical reference for agent task/PR/verify/commit operations. Agent instructions should point here instead of embedding specific command strings.

## Agent cheat sheet

Operation | Command
--- | ---
PLANNER: list/show tasks | `python .codex-swarm/agentctl.py task list` / `python .codex-swarm/agentctl.py task show <task-id>`
PLANNER: add/update task | `python .codex-swarm/agentctl.py task add <task-id> ...` / `python .codex-swarm/agentctl.py task update <task-id> ...`
PLANNER: scaffold artifact | `python .codex-swarm/agentctl.py task scaffold <task-id>`
CODER/TESTER/DOCS: start checkout (branch_pr) | `python .codex-swarm/agentctl.py work start <task-id> --agent <ROLE> --slug <slug> --worktree`
CODER/TESTER/DOCS: update PR artifacts | `python .codex-swarm/agentctl.py pr update <task-id>`
CODER/TESTER/DOCS/REVIEWER: add handoff note | `python .codex-swarm/agentctl.py pr note <task-id> --author <ROLE> --body \"...\"`
CODER/TESTER: verify task | `python .codex-swarm/agentctl.py verify <task-id>`
REVIEWER: check PR artifacts | `python .codex-swarm/agentctl.py pr check <task-id>`
INTEGRATOR: integrate task | `python .codex-swarm/agentctl.py integrate <task-id> --branch task/<task-id>/<slug> --merge-strategy squash --run-verify`
INTEGRATOR: finish task(s) | `python .codex-swarm/agentctl.py finish <task-id> [<task-id> ...] --commit <git-rev> --author INTEGRATOR --body \"Verified: ...\"`
INTEGRATOR: commit closure | `python .codex-swarm/agentctl.py commit <task-id> -m \"✅ <task-id> close ...\" --auto-allow --allow-tasks --require-clean`

## Common commands

```bash
# list/show
python .codex-swarm/agentctl.py task list
python .codex-swarm/agentctl.py task show <task-id>

# validate .codex-swarm/tasks.json (schema/deps/checksum)
python .codex-swarm/agentctl.py task lint

# normalize task READMEs via backend rewrite
python .codex-swarm/agentctl.py task normalize

# readiness gate (deps DONE)
python .codex-swarm/agentctl.py ready <task-id>

# status transitions that require structured comments
python .codex-swarm/agentctl.py start <task-id> --author CODER --body "Start: ... (why, scope, plan, risks)"
python .codex-swarm/agentctl.py block <task-id> --author CODER --body "Blocked: ... (what blocks, next step, owner)"

# run per-task verify commands (declared on the task)
python .codex-swarm/agentctl.py verify <task-id> --skip-if-unchanged
# (when .codex-swarm/tasks/<task-id>/pr/verify.log exists, agentctl will append to it by default)

# before committing, validate staged allowlist + message quality
python .codex-swarm/agentctl.py guard commit <task-id> -m "✨ <task-id> Short meaningful summary" --auto-allow

# if you want a safe wrapper that also runs `git commit`
python .codex-swarm/agentctl.py commit <task-id> -m "✨ <task-id> Short meaningful summary" --allow <path-prefix>

# when closing a task in the branching workflow (INTEGRATOR on the base branch)
python .codex-swarm/agentctl.py finish <task-id> --commit <git-rev> --author INTEGRATOR --body "Verified: ... (what ran, results, caveats)"
# batch close (same commit metadata + comment applied to each task)
python .codex-swarm/agentctl.py finish <task-id> <task-id> --commit <git-rev> --author INTEGRATOR --body "Verified: ... (what ran, results, caveats)"
```

```bash
# batch add (shared metadata for each task)
python .codex-swarm/agentctl.py task add <task-id> <task-id> --title "..." --description "..." --priority med --owner CODER
```

## Commit naming for batch finish

Include every task ID in the commit subject (full id or suffix after the last dash), for example: `✅ <suffix> <suffix> close ...`.

## Branching workflow helpers

```bash
# one-command task checkout (branch + worktree + PR artifact + docs skeleton)
python .codex-swarm/agentctl.py work start <task-id> --agent CODER --slug <slug> --worktree

# create a task branch + worktree (inside this repo only)
# - branch: task/<task-id>/<slug>
# - worktree: .codex-swarm/worktrees/<task-id>-<slug>/
python .codex-swarm/agentctl.py branch create <task-id> --agent CODER --slug <slug> --worktree

# show quick status (ahead/behind, worktree path)
python .codex-swarm/agentctl.py branch status --branch task/<task-id>/<slug>

# open/update/check the tracked PR artifact (local PR simulation)
python .codex-swarm/agentctl.py pr open <task-id> --branch task/<task-id>/<slug> --author CODER
python .codex-swarm/agentctl.py pr update <task-id>  # optional; integrate refreshes diffstat + README auto-summary on the base branch
python .codex-swarm/agentctl.py pr check <task-id>
python .codex-swarm/agentctl.py pr note <task-id> --author CODER --body "Handoff: ..."

# integrate into the base branch (INTEGRATOR only; run from repo root on the base branch)
# includes: pr check → verify (skips if already verified for the same SHA unless --run-verify) → merge → refresh diffstat/README auto-summary → finish → task lint
python .codex-swarm/agentctl.py integrate <task-id> --branch task/<task-id>/<slug> --merge-strategy squash --run-verify
python .codex-swarm/agentctl.py integrate <task-id> --branch task/<task-id>/<slug> --merge-strategy squash --dry-run

# cleanup merged branches/worktrees (dry-run by default)
python .codex-swarm/agentctl.py cleanup merged
python .codex-swarm/agentctl.py cleanup merged --yes
```

## Ergonomics helpers

```bash
# find tasks that are ready to start (deps DONE)
python .codex-swarm/agentctl.py task next

# search tasks by text (title/description/tags/comments)
python .codex-swarm/agentctl.py task search agentctl

# scaffold a workflow artifact (.codex-swarm/tasks/<task-id>/README.md)
python .codex-swarm/agentctl.py task scaffold <task-id>

# suggest minimal --allow prefixes based on staged files
python .codex-swarm/agentctl.py guard suggest-allow
python .codex-swarm/agentctl.py guard suggest-allow --format args
```

## Workflow reminders

- `.codex-swarm/tasks.json` is canonical; agents are forbidden from editing it by hand (use agentctl only).
- Before finishing a task, ensure @.codex-swarm/tasks/<task-id>/README.md is filled in (no placeholder `...`).
- In branching workflow, `agentctl` rejects .codex-swarm/tasks.json writes outside the repo root checkout on the pinned base branch (and guardrails reject committing .codex-swarm/tasks.json from task branches).
- Keep work atomic: one task → one implementation commit (plus planning + closure commits if you use the 3-phase cadence).
- Prefer `start/block/finish` over `task set-status`.
- Keep allowlists tight: pass only the path prefixes you intend to commit.

## Workflow mode

`agentctl` behavior is controlled by `.codex-swarm/config.json`:

- `workflow_mode: "direct"`: low-ceremony, single-checkout workflow.
  - Do all work in the current checkout; do not create task branches/worktrees (`agentctl branch create` is refused).
  - `python .codex-swarm/agentctl.py work start <task-id>` only scaffolds `.codex-swarm/tasks/<task-id>/README.md` (it does not create a branch/worktree).
  - PR artifacts under `.codex-swarm/tasks/<task-id>/pr/` are optional.
  - Tasks can be implemented and closed on the current branch; `.codex-swarm/tasks.json` is still updated only via `python .codex-swarm/agentctl.py` (no manual edits).
- `workflow_mode: "branch_pr"`: strict branching workflow (task branches + worktrees + tracked PR artifacts + single-writer `.codex-swarm/tasks.json`).
  - Planning and closure happen in the repo root checkout on `main`; `.codex-swarm/tasks.json` is never modified/committed on task branches.
  - Executors work in `.codex-swarm/worktrees/<task-id>-<slug>/` on `task/<task-id>/<slug>`.
  - Each task uses tracked PR artifacts under `.codex-swarm/tasks/<task-id>/pr/`.
  - Integration/closure is performed only by INTEGRATOR via `python .codex-swarm/agentctl.py integrate` / `python .codex-swarm/agentctl.py finish`.

In `branch_pr`, executors leave handoff notes in `.codex-swarm/tasks/<task-id>/pr/review.md` (under `## Handoff Notes`), and INTEGRATOR appends them to `.codex-swarm/tasks.json` at closure.

## Base branch

By default, `agentctl` uses a pinned “base branch” as the mainline for branch/worktree creation and integration. Pinning happens automatically on first run:

- If `git config --get codexswarm.baseBranch` is unset and the current branch is not a task branch, `agentctl` sets it to the current branch.
- You can override it explicitly per command via `--base`, or persistently via `.codex-swarm/config.json` → `base_branch`.

Useful commands:

```bash
git config --get codexswarm.baseBranch
git config --local codexswarm.baseBranch <branch>
git config --unset codexswarm.baseBranch
```
