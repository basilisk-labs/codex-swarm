# Legacy PR Artifacts (deprecated)

`.codex-swarm/workspace/prs/` is the legacy location for tracked PR-like artifacts.

## Current location

For task `T-123`, tracked PR artifacts now live under the per-task directory:

- Canonical task/PR doc: `.codex-swarm/workspace/T-123/README.md`
- PR artifacts: `.codex-swarm/workspace/T-123/pr/{meta.json,diffstat.txt,verify.log,review.md}`

## Notes

- New tasks should not create anything under `.codex-swarm/workspace/prs/`.
- `python .codex-swarm/agentctl.py` still supports reading legacy artifacts during migration, but the default layout is `.codex-swarm/workspace/T-###/pr/`.
