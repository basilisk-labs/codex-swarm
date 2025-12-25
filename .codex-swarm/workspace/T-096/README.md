# T-096: Centralize agentctl guidance

## Summary

- Centralized agentctl operational guidance in @.codex-swarm/agentctl.md and aligned agent instructions to reference it.

## Goal

- Reduce duplicated command strings across agent specs by making agentctl.md the single source of truth.

## Scope

- Updated @.codex-swarm/agentctl.md with an agent cheat sheet and source-of-truth note.
- Reworded agent JSON instructions to reference agentctl.md instead of embedding command strings.

## Risks

- Low: documentation-only changes; risk is confusion if agentctl.md drifts.

## Verify Steps

- `python3 .codex-swarm/agentctl.py task lint`

## Rollback Plan

- Revert the commits for T-096 and restore previous agent instruction text.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
