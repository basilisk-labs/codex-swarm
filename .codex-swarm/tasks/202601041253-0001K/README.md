---
id: "202601041253-0001K"
title: "Remove legacy tasks.py + migrate docs to agentctl"
status: "DONE"
priority: "high"
owner: "CODER"
tags: ["docs", "workflow", "tooling"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py agents"]
commit: { hash: "d6517d61191b4d80e80acc63117b6e55ba02c557", message: "Legacy completion (backfill)" }
comments:
  - { author: "PLANNER", body: "Planned: remove legacy tasks.py + update docs to agentctl; Constraints: no manual tasks.json edits; keep guidance consistent across repo." }
  - { author: "CODER", body: "Start: remove scripts/tasks.py; update README + other docs to new agentctl workflow; Constraints: no manual tasks.json edits; keep changes minimal and consistent." }
  - { author: "REVIEWER", body: "Verified: scripts/tasks.py removed; README.md and GUIDELINE.md updated to agentctl-based task lifecycle (ready/start/block/task/verify/guard/finish); agentctl task lint passes; Limitations: existing CODEX owner warnings remain." }
doc_version: 2
doc_updated_at: "2026-01-11T08:06:07+00:00"
doc_updated_by: "agentctl"
description: "Delete scripts/tasks.py and update README.md + any other docs/configs that mention the old tasks.py/status-board flow, replacing it with the agentctl CLI workflow (ready/start/block/task/verify/guard/finish)."
dirty: false
redmine_id: 331
---
