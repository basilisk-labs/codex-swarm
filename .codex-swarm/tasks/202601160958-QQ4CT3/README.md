---
id: "202601160958-QQ4CT3"
title: "Automate framework upgrades"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-16T10:16:11+00:00"
doc_updated_by: "agentctl"
description: "Track last update date, add automatic refresh from https://github.com/basilisk-labs/codex-swarm when stale or forced, and surface the workflow via agentctl plus a dedicated agent. Downstream tasks: 202601160958-DAS67K (UPGRADER agent design), 202601160958-NV8M5V (agentctl automation), 202601160958-AM3G42 (tests)."
---
## Summary
- Automate framework updates by recording the last refresh date, honoring a 10-day staleness threshold, and providing an `agentctl upgrade` command backed by the UPGRADER agent.

## Context
- Maintaining parity with https://github.com/basilisk-labs/codex-swarm keeps our workflow fresh; this task stitches together the agent spec, CLI automation, and tests.

## Scope
- Define the UPGRADER agent (202601160958-DAS67K) so the purpose and guards are clear.
- Extend agentctl and config metadata (202601160958-NV8M5V) so the command runs safely and logs the new timestamp.
- Add regression tests (202601160958-AM3G42) so staleness math is vetted before we rely on it.

## Risks
- Git operations require clean main; automation must refuse to run in dirty states to avoid mixing unrelated work.
- Upstream remote must stay accessible; documented fallback is to re-run the upgrade manually.

## Verify Steps
- `python3 -m unittest tests.test_framework_upgrade`
- (Optional) `python .codex-swarm/agentctl.py upgrade --force` on a clean base branch after ensuring this repo can fast-forward from the upstream.

## Rollback Plan
- Revert the code, tests, docs, and config addition created by the sub-tasks if the automation misbehaves.
- Restore `.codex-swarm/config.json` to its prior shape and rerun `git reset --hard` on main to wipe the upgrade commit.

## Notes
- Task PR artifacts under `.codex-swarm/tasks/<task-id>/pr/` will record the last verify log and diff whenever these tasks go through the usual branch_pr workflow.

