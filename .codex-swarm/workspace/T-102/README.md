# T-102: Harden agentctl depends_on parsing

## Summary

- Filter out literal "[]" and empty strings from depends_on during task add/update.

## Goal

- Prevent invalid depends_on entries created by misuse of --depends-on.

## Scope

- Adjust depends_on normalization in agentctl task add/update.
- Fix docs examples that encouraged passing --depends-on "[]".

## Risks

- Low: only affects task add/update input parsing.

## Verify Steps

- python3 .codex-swarm/agentctl.py task add T-999 --title "Test" --description "Test" --priority low --owner DOCS

## Rollback Plan

- Revert this task's commits to restore prior depends_on handling.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- .codex-swarm/agentctl.py: ignore "[]" and empty depends_on values on add/update.
- docs/commands.md: remove --depends-on "[]" example.
- docs/tasks-and-agentctl.md: remove --depends-on "[]" example.
<!-- END AUTO SUMMARY -->
