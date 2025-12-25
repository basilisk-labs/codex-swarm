# T-089: Refactor workflow paths

## Summary

- Moved agentctl, config, tasks, and workflow artifacts under `.codex-swarm` and updated live docs/configs.

## Goal

- Consolidate framework paths under `.codex-swarm` without rewriting historical task text.

## Scope

- Move `scripts/agentctl.py` to `.codex-swarm/agentctl.py`.
- Rename `.codex-swarm/swarm.config.json` to `.codex-swarm/config.json`.
- Move `tasks.json` to `.codex-swarm/tasks.json`.
- Move `docs/workflow/` to `.codex-swarm/workspace/`.
- Update framework docs, agent prompts, config, `agentctl.py`, `tasks.html`, and `clean.sh` references.

## Risks

- Potential missed path references in non-framework files.

## Verify Steps

- (not run) `python3 .codex-swarm/agentctl.py --help`

## Rollback Plan

- Revert the commit to restore original paths.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (not auto-updated)
<!-- END AUTO SUMMARY -->
