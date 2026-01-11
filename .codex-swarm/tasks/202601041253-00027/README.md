---
id: "202601041253-00027"
title: "Require explicit depends_on on task add"
status: "DONE"
priority: "med"
owner: "PLANNER"
tags: ["workflow", "tasks", "dependencies"]
verify: ["python scripts/agentctl.py agents", "python scripts/agentctl.py task lint"]
commit: { hash: "dea6792a39f57fd3f842a06efa198525afc7271d", message: "Legacy completion (backfill)" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/prs/T-071." }
description: "Update the agent pipeline instructions so every task added to tasks.json includes an explicit depends_on list (use [] when there are no dependencies). Update AGENTS.md schema/docs and PLANNER workflow to require setting dependencies (and to ask for clarification when dependencies are unknown)."
dirty: false
redmine_id: 351
---
