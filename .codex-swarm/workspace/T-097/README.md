# T-097: Rename docs index and update references

## Summary

- Renamed the docs index to `docs/README.md`, updated README references, and clarified that `clean.sh` removes `docs/`.

## Goal

- Make the docs entrypoint conventional and keep references consistent.

## Scope

- `docs/index.md` -> `docs/README.md` rename.
- Update README docs links and repository layout.
- Clarify `clean.sh` comment about removing `docs/`.

## Risks

- Stale references if documentation filenames change without updating README.

## Verify Steps

- Manual check that all referenced doc paths exist.

## Rollback Plan

- Revert this commit to restore the previous filenames and references.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- Renamed docs index to `docs/README.md`.
- Updated `README.md` references.
- Clarified `clean.sh` documentation note.
<!-- END AUTO SUMMARY -->
