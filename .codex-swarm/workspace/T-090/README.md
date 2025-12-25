# T-090: Move ORCHESTRATOR spec into JSON

## Summary

- Moved the ORCHESTRATOR spec into a JSON agent definition.
- Updated global docs to reference the JSON spec location and start-of-run rule.

## Goal

- Keep agent specs in JSON while preserving ORCHESTRATOR start-of-run requirements.

## Scope

- Add `.codex-swarm/agents/ORCHESTRATOR.json`.
- Update `AGENTS.md` and `README.md` references to the ORCHESTRATOR spec.

## Risks

- Low: documentation-only change; no runtime behavior change.

## Verify Steps

- Not run (docs/metadata changes only).

## Rollback Plan

- Revert the commits `19c4c5c` and `b3ab294`.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- Added `.codex-swarm/agents/ORCHESTRATOR.json`.
- Updated `AGENTS.md`.
- Updated `README.md`.
<!-- END AUTO SUMMARY -->
