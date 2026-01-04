---
id: "202601041253-0002M"
title: "Agents: prefer agentctl CLI for supported operations"
status: "DONE"
priority: "high"
owner: "PLANNER"
depends_on: ["202601041253-0002A", "202601041253-0002K"]
tags: ["agents", "agentctl", "workflow"]
verify: ["python scripts/agentctl.py task lint"]
commit: { hash: "95358c3c7df46275d7afccb5e2556aa52cdb4c39", message: "🧾 T-084 fill workflow README" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/T-084/pr." }
description: "Audit scripts/agentctl.py capabilities and update .codex-swarm/agents/*.json prompts so each agent uses agentctl for any supported operation (tasks.json ops, branch/worktree management, PR artifacts, verify logs, commit guardrails, integrate/cleanup). Only fall back to raw git/shell commands when agentctl has no equivalent."
dirty: false
redmine_id: 364
---
