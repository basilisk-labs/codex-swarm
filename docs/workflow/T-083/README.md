# T-083: Docs: fix README Mermaid parse on GitHub

## Summary

- Fix the Mermaid diagrams in `README.md` so they render correctly on GitHub.

## Goal

- Remove Mermaid parse errors in GitHub’s renderer for the Architecture & Workflow diagrams.

## Scope

- `README.md`: adjust Mermaid syntax/labels for GitHub compatibility (no behavioral changes).

## Risks

- Very low; docs-only change.

## Verify Steps

- `python scripts/agentctl.py task lint`
- Preview `README.md` on GitHub and confirm Mermaid blocks render.

## Rollback Plan

- Revert the doc commit.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `docs/workflow/T-083/pr/diffstat.txt`
- `docs/workflow/T-083/pr/meta.json`
- `docs/workflow/T-083/pr/review.md`
- `docs/workflow/T-083/pr/verify.log`
<!-- END AUTO SUMMARY -->
