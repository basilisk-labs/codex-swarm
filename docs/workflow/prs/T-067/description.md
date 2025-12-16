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
- `docs/workflow/T-064.md`
- `docs/workflow/T-067.md`
- `docs/workflow/prs/README.md`
- `docs/workflow/prs/T-067/description.md`
- `docs/workflow/prs/T-067/diffstat.txt`
- `docs/workflow/prs/T-067/meta.json`
- `docs/workflow/prs/T-067/review.md`
- `docs/workflow/prs/T-067/verify.log`
- `scripts/agentctl.py`
<!-- END AUTO SUMMARY -->
