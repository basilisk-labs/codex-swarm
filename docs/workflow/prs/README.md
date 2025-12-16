# Legacy PR Artifacts (deprecated)

`docs/workflow/prs/` is the legacy location for tracked PR-like artifacts.

## Current location

For task `T-123`, tracked PR artifacts now live under the per-task directory:

- Canonical task/PR doc: `docs/workflow/T-123/README.md`
- PR artifacts: `docs/workflow/T-123/pr/{meta.json,diffstat.txt,verify.log,review.md}`

## Notes

- New tasks should not create anything under `docs/workflow/prs/`.
- `python scripts/agentctl.py` still supports reading legacy artifacts during migration, but the default layout is `docs/workflow/T-###/pr/`.
