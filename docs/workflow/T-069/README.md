# T-069: agentctl pr note: append handoff notes

## Summary

- Add `agentctl pr note` to append correctly formatted handoff notes under `## Handoff Notes` in `docs/workflow/T-###/pr/review.md`.

## Scope

- `scripts/agentctl.py`: add `pr note` subcommand to append `- ROLE: TEXT` under the right section with stable formatting and clear errors.
- `.codex-swarm/agentctl.md`: document the new helper.

## Risks

- None expected; behavior is additive and only touches PR artifacts when invoked.

## Verify Steps

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke: `python scripts/agentctl.py pr note T-069 --author CODER --body \"...\"` and confirm `docs/workflow/T-069/pr/review.md` updates.

## Rollback Plan

- Revert this task branch.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

## Task Notes (legacy)

## Goal

- Reduce PR review friction by adding a safe helper to append handoff notes in a consistent format.

## Scope

- `scripts/agentctl.py`:
  - Add `pr note` subcommand:
    - `python scripts/agentctl.py pr note T-### --author ROLE --body TEXT`
    - Appends a bullet under `## Handoff Notes` in `docs/workflow/T-###/pr/review.md` as `- ROLE: TEXT`.
    - Fails with a clear “Fix:” message when the PR artifact is missing (or optionally creates the skeleton if that matches the existing workflow rules).
- Docs:
  - Update `.codex-swarm/agentctl.md` (and optionally `docs/workflow/prs/README.md`) to recommend `pr note` for handoff notes.

## Verification

- `python -m compileall scripts/agentctl.py`
- `python scripts/agentctl.py task lint`
- Manual smoke:
  - Create/open a PR artifact and run `python scripts/agentctl.py pr note T-### --author CODER --body \"...\"`, then confirm `docs/workflow/T-###/pr/review.md` is updated correctly.
