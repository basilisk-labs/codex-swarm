# T-082: Docs: update README and fix Mermaid diagram

## Summary

- Update the root `README.md` to match the current `branch_pr` workflow and recent `agentctl` improvements; fix Mermaid diagrams to render on GitHub.

## Goal

- Keep the top-level project documentation accurate and copy/paste-friendly for new contributors.

## Scope

- `README.md`:
  - Update workflow text to mention `integrate` auto-refreshing PR artifacts.
  - Update workflow text to mention `integrate` can skip redundant verify when SHA is already verified (and `--run-verify` forces rerun).
  - Fix Mermaid diagram(s) to avoid GitHub rendering issues.

## Risks

- Low. Documentation-only change, but Mermaid edits must remain syntactically valid.

## Verify Steps

- `python scripts/agentctl.py task lint`
- Manually preview `README.md` in GitHub (Mermaid blocks render).

## Rollback Plan

- Revert the doc commit.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `docs/workflow/T-082/pr/diffstat.txt`
- `docs/workflow/T-082/pr/meta.json`
- `docs/workflow/T-082/pr/review.md`
- `docs/workflow/T-082/pr/verify.log`
<!-- END AUTO SUMMARY -->
