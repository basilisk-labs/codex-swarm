# T-069: agentctl pr note: append handoff notes

## Summary

- Add `agentctl pr note` to append correctly formatted handoff notes under `## Handoff Notes` in `docs/workflow/prs/T-###/review.md`.

## Scope

- `scripts/agentctl.py`: add `pr note` subcommand to append `- ROLE: TEXT` under the right section with stable formatting and clear errors.
- `.codex-swarm/agentctl.md`: document the new helper.

## Risks

- None expected; behavior is additive and only touches PR artifacts when invoked.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: `python scripts/agentctl.py pr note T-069 --author CODER --body \"...\"` and confirm `docs/workflow/prs/T-069/review.md` updates.

## Rollback Plan

- Revert this task branch.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
