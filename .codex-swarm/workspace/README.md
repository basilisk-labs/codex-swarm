# Workflow Artifacts

Each completed task should have an atomic documentation artifact under this folder.

For local PR-like review and integration artifacts, see `.codex-swarm/workspace/T-###/pr/`.

## Naming

- `T-###/README.md` (example: `.codex-swarm/workspace/T-025/README.md`)
- PR artifact (branch_pr): `.codex-swarm/workspace/T-###/pr/{meta.json,diffstat.txt,verify.log,review.md}`

## Purpose

Capture what was implemented for the task in a small, reviewable, and durable artifact.

## Suggested Template

- Title (`T-###: <short summary>`)
- Scope (what changed / what did not change)
- Files touched (key @paths)
- Behavior / UX notes (if user-visible)
- Verification (commands that were run, or how to validate locally)
- Follow-ups / known gaps (if any)
