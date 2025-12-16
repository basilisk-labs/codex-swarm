# agentctl quickstart

`python scripts/agentctl.py` is the only supported way to inspect/update `tasks.json` (manual edits break the checksum).

## Common commands

```bash
# list/show
python scripts/agentctl.py task list
python scripts/agentctl.py task show T-123

# validate tasks.json (schema/deps/checksum)
python scripts/agentctl.py task lint

# readiness gate (deps DONE)
python scripts/agentctl.py ready T-123

# status transitions that require structured comments
python scripts/agentctl.py start T-123 --author CODER --body "Start: ... (why, scope, plan, risks)"
python scripts/agentctl.py block T-123 --author CODER --body "Blocked: ... (what blocks, next step, owner)"

# run per-task verify commands (declared on the task)
python scripts/agentctl.py verify T-123 --skip-if-unchanged
# (when docs/workflow/T-123/pr/verify.log exists, agentctl will append to it by default)

# before committing, validate staged allowlist + message quality
python scripts/agentctl.py guard commit T-123 -m "✨ T-123 Short meaningful summary" --auto-allow

# if you want a safe wrapper that also runs `git commit`
python scripts/agentctl.py commit T-123 -m "✨ T-123 Short meaningful summary" --allow <path-prefix>

# when closing a task in the branching workflow (INTEGRATOR on main)
python scripts/agentctl.py finish T-123 --commit <git-rev> --author INTEGRATOR --body "Verified: ... (what ran, results, caveats)"
```

## Branching workflow helpers

```bash
# one-command task checkout (branch + worktree + PR artifact + docs skeleton)
python scripts/agentctl.py work start T-123 --agent CODER --slug <slug> --worktree

# create a task branch + worktree (inside this repo only)
# - branch: task/T-123/<slug>
# - worktree: .codex-swarm/worktrees/T-123-<slug>/
python scripts/agentctl.py branch create T-123 --agent CODER --slug <slug> --worktree

# show quick status (ahead/behind, worktree path)
python scripts/agentctl.py branch status --branch task/T-123/<slug> --base main

# open/update/check the tracked PR artifact (local PR simulation)
python scripts/agentctl.py pr open T-123 --branch task/T-123/<slug> --author CODER
python scripts/agentctl.py pr update T-123  # optional; integrate refreshes diffstat + README auto-summary on main
python scripts/agentctl.py pr check T-123
python scripts/agentctl.py pr note T-123 --author CODER --body "Handoff: ..."

# integrate into main (INTEGRATOR only; run from repo root on main)
# includes: pr check → verify (skips if already verified for the same SHA unless --run-verify) → merge → refresh diffstat/README auto-summary → finish → task lint
python scripts/agentctl.py integrate T-123 --branch task/T-123/<slug> --merge-strategy squash --run-verify
python scripts/agentctl.py integrate T-123 --branch task/T-123/<slug> --merge-strategy squash --dry-run

# cleanup merged branches/worktrees (dry-run by default)
python scripts/agentctl.py cleanup merged
python scripts/agentctl.py cleanup merged --yes
```

## Ergonomics helpers

```bash
# find tasks that are ready to start (deps DONE)
python scripts/agentctl.py task next

# search tasks by text (title/description/tags/comments)
python scripts/agentctl.py task search agentctl

# scaffold a workflow artifact (docs/workflow/T-###/README.md)
python scripts/agentctl.py task scaffold T-123

# suggest minimal --allow prefixes based on staged files
python scripts/agentctl.py guard suggest-allow
python scripts/agentctl.py guard suggest-allow --format args
```

## Workflow reminders

- `tasks.json` is canonical; do not edit it by hand.
- In branching workflow, `agentctl` rejects tasks.json writes outside the repo root checkout on `main` (and guardrails reject committing tasks.json from task branches).
- Keep work atomic: one task → one implementation commit (plus planning + closure commits if you use the 3-phase cadence).
- Prefer `start/block/finish` over `task set-status`.
- Keep allowlists tight: pass only the path prefixes you intend to commit.

## Workflow mode

`agentctl` behavior is controlled by `.codex-swarm/swarm.config.json`:

- `workflow_mode: "direct"`: legacy mode (minimal branch guardrails)
- `workflow_mode: "branch_pr"`: task branches + worktrees + PR artifacts + single-writer `tasks.json`

In `branch_pr`, executors leave handoff notes in `docs/workflow/T-###/pr/review.md` (under `## Handoff Notes`), and INTEGRATOR appends them to `tasks.json` at closure.
