---
id: "202601160958-AM3G42"
title: "Test framework update workflow"
status: "TODO"
priority: "med"
owner: "TESTER"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-16T10:16:04+00:00"
doc_updated_by: "agentctl"
description: "Add regression coverage for the 10-day staleness threshold and forced refresh path, ensuring the agentctl command exercises the new logic and the behavior is documented for downstream agents."
---
## Summary
- Capture the regression coverage that proves the new staleness math and config parsing behave as expected before relying on them for upgrades.

## Context
- `tests/test_framework_upgrade.py` exercises the helper utilities used by the CLI upgrade flow, so its README should describe what that file covers and why it matters.

## Scope
- Document that the suite imports `.codex-swarm/agentctl.py`, mocks the config, and asserts the staleness threshold and ISO parsing logic.
- Mention that the log is kept minimal on purpose to keep CI fast.

## Risks
- The tests currently rely on the repo being importable as a module; if agentctl gains heavy dependencies, the suite may need stubbing or isolation.

## Verify Steps
- Run `python3 -m unittest tests.test_framework_upgrade` (headless, fast, and now part of the documented process).

## Rollback Plan
- Remove the test file and its entry from the CI/test suite if it starts leaking state into other modules.

## Notes
- Future end-to-end coverage may run `agentctl upgrade` in a sandbox, but for now this unit suite provides confidence that the helpers behave.

