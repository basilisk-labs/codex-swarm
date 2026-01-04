# T-108: Docs: modular backends + local tasks model

## Summary

- Document the backend-driven source-of-truth model (local vs redmine) and new task ID format.
- Describe offline fallback, sync behavior, and exported `tasks.json` usage.

## Goal

- Provide clear, backend-aware documentation that matches the planned architecture and CLI behavior.

## Scope

- Update docs to explain:
  - Backend selection and plugin configs.
  - Local task storage + frontmatter format.
  - Redmine canonical behavior with auto offline fallback and conflict diff.
  - Exported `tasks.json` as a snapshot for `tasks.html`.

## Risks

- Docs may drift from implementation if code changes lag behind.
- External links or examples may become stale if the ID format changes again.

## Verify Steps

- Run `rg -n "tasks-and-agentctl|workspace" docs README.md` to ensure old references are removed.
- Check that all docs links resolve after renaming.

## Rollback Plan

- Revert the documentation changes in `docs/` and `README.md`.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
