# T-109: Docs: modularize + numbered docs

## Summary

- Rename docs with sequential numbers and update references.
- Expand docs with modular structure and planned content sections.

## Goal

- Make the documentation easier to navigate and maintain with a numbered, modular layout.

## Scope

- Rename `docs/*.md` to `docs/NN-*.md` (keep `docs/README.md` as the index).
- Update internal links in docs and root `README.md`.
- Add structured “Planned Expansions” sections to encourage modular growth.

## Risks

- Link drift if any references to old filenames remain.
- External references (outside repo) may break due to renames.

## Verify Steps

- Run `rg -n "overview.md|workflow.md|tasks-and-agentctl.md" docs README.md` to confirm no old names remain.
- Open `docs/README.md` and verify the ordered list matches actual filenames.

## Rollback Plan

- Revert the rename commits and restore original docs filenames.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
