---
id: "202601041253-0002P"
title: "Define workflow_mode variants (direct vs branch_pr)"
status: "DONE"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["workflow", "docs", "agents"]
verify: ["python scripts/agentctl.py task lint"]
commit: "2b93d6297c22494b1cbc0805952a6f81b3461153"
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/T-086/pr." }
description: "Add a clear, unambiguous definition of workflow_mode values \\\"direct\\\" and \\\"branch_pr\\\" across agent instructions and documentation. Document the operational differences (where work happens, whether task branches/worktrees are required, who can write tasks.json, required PR artifacts under docs/workflow/T-###/pr, and which agent is allowed to integrate/finish). Update AGENTS.md and .codex-swarm/agentctl.md accordingly."
dirty: false
redmine_id: 366
---
