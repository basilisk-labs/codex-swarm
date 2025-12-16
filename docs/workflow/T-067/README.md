# T-067: Align agentctl with branch_pr spec (worktrees, PR checks, integrate)

## Summary

- Bring `agentctl` in line with the stricter `workflow_mode=branch_pr` spec: standardized task branch naming, `.codex-swarm/worktrees/` root, strict PR artifact validation, and a one-button `integrate` that runs check → verify → merge → finish.

## Scope

- Add `.codex-swarm/swarm.config.json` with `workflow_mode: branch_pr`.
- Update `agentctl`:
  - `branch create` signature + behavior (`--agent`, fixed `task/T-###/<slug>` naming, `.codex-swarm/worktrees/`, `--reuse`).
  - New `branch status`.
  - `pr open/update/check` stricter rules (required sections + non-empty, clean-tree requirement, tasks.json diff guard).
  - `integrate` with `--dry-run`, merge strategies (`squash|merge|rebase`), verify execution in the branch worktree (or temp worktree), and automatic `finish` + `task lint`.
  - `verify --cwd` support.
- Update docs and agent role instructions to match the new workflow conventions.

## Risks

- Stricter checks may break older “direct” habits; guarded by `.codex-swarm/swarm.config.json` toggle.
- `integrate` performs `finish` (writes `tasks.json`) automatically in `branch_pr` mode; requires running on clean `main` from repo root.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py branch --help`
- `python scripts/agentctl.py pr --help`
- `python scripts/agentctl.py integrate --help`

## Rollback Plan

- Revert this branch.
- Set `.codex-swarm/swarm.config.json` back to `workflow_mode: direct` to disable `branch_pr` enforcement.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/agentctl.md`
- `.codex-swarm/agents/CODER.json`
- `.codex-swarm/agents/DOCS.json`
- `.codex-swarm/agents/INTEGRATOR.json`
- `.codex-swarm/agents/REVIEWER.json`
- `.codex-swarm/agents/TESTER.json`
- `.codex-swarm/swarm.config.json`
- `AGENTS.md`
- `README.md`
- `docs/workflow/T-064/README.md`
- `docs/workflow/T-067/README.md`
- `docs/workflow/prs/README.md` (legacy)
- `docs/workflow/T-067/pr/description.md`
- `docs/workflow/T-067/pr/diffstat.txt`
- `docs/workflow/T-067/pr/meta.json`
- `docs/workflow/T-067/pr/review.md`
- `docs/workflow/T-067/pr/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->

## Task Notes (legacy)

## Goal

- Bring `python scripts/agentctl.py` in line with the stricter `branch_pr` workflow spec:
  - task branches + worktrees rooted at `.codex-swarm/worktrees/`
  - PR artifacts under `docs/workflow/T-###/pr/` with strict validation
  - one-button integration (check → verify → merge → finish) for INTEGRATOR
  - standardized command output + anti-footgun errors

## Scope

- `agentctl` commands:
  - `branch create` spec compliance (naming, worktree root, reuse checks, ignore checks).
  - New `branch status`.
  - `pr open/update/check` spec compliance (files, meta fields, required sections + non-empty content).
  - `integrate` improvements: `--dry-run`, merge strategies incl. `rebase`, verify run in branch worktree, meta updates.
  - `finish` guardrails for `branch_pr` (main-only, not in worktrees, author allowlist, require PR + pr check).
  - `guard commit` branch_pr guardrails (tasks.json protection, branch ↔ task id enforcement with exceptions for closure on main).
  - `verify` support for running in a specific checkout (`--cwd`).
- Config:
  - Add `.codex-swarm/swarm.config.json` to enable `workflow_mode=branch_pr`.
- Docs:
  - Update existing workflow docs to use `.codex-swarm/worktrees/` and the normalized branch naming.

## Verification

- `python scripts/agentctl.py task lint`
- `python -m compileall scripts/agentctl.py`
- Manual smoke:
  - `python scripts/agentctl.py branch create T-067 --agent CODER --slug smoke --worktree`
  - `python scripts/agentctl.py pr open T-067 --branch task/T-067/smoke --author CODER`
  - `python scripts/agentctl.py pr check T-067 --branch task/T-067/smoke`
  - `python scripts/agentctl.py integrate T-067 --branch task/T-067/smoke --dry-run`

## Outcome

- `workflow_mode` config is now consolidated to `.codex-swarm/swarm.config.json` and `branch_pr` enforcement is enabled there.
- Worktrees are rooted at `.codex-swarm/worktrees/`, and PR artifacts are tracked under `docs/workflow/T-###/pr/`.
- `tasks.json` updates for closure are now gated to `main`, and handoff notes are captured in `docs/workflow/T-###/pr/review.md` and appended at `finish`.

## Commits

- Planning: `0a08f61` (main)
- Implementation: `91b3760` (main)
- Closure: (this commit) marks `T-067` DONE and syncs docs
