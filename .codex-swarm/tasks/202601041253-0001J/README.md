---
id: "202601041253-0001J"
title: "Adopt agentctl-based agent workflow"
status: "DONE"
priority: "high"
owner: "CODER"
tags: ["agents", "workflow", "tooling"]
verify: ["python scripts/agentctl.py agents"]
commit: { hash: "8f6ecd8bd1a461e52243f90732530069652a45c1", message: "🛠️ T-050 Adopt agentctl workflow" }
comments:
  - { author: "PLANNER", body: "Planned: migrate agent workflow to agentctl CLI; Constraints: local repo only; No manual tasks.json edits." }
  - { author: "CODER", body: "Start: update AGENTS.md and .AGENTS/*.json to use agentctl; add scripts/agentctl.py; make tasks.json lint-clean; Constraints: no manual tasks.json edits." }
  - { author: "REVIEWER", body: "Verified: agentctl task lint passes; AGENTS.md/.AGENTS now require agentctl for task ops; scripts/agentctl.py is tracked; Limitations: existing CODEX owner warnings remain." }
description: "Update AGENTS.md + .AGENTS/*.json to use scripts/agentctl.py for task operations (no manual tasks.json edits), add the new CLI to the repo, and make tasks.json pass agentctl task lint (meta+checksum, DONE tasks have commit metadata)."
dirty: false
redmine_id: 330
---
