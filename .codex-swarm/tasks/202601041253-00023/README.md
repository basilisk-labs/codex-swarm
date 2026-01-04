---
id: "202601041253-00023"
title: "Align agentctl with branch_pr spec (worktrees, PR checks, integrate)"
status: "DONE"
priority: "med"
owner: "PLANNER"
tags: ["agentctl", "workflow", "git"]
verify: ["python scripts/agentctl.py task lint", "python -m compileall scripts/agentctl.py"]
commit: { hash: "91b3760239846f01443b8550c9402dcc99c12c74", message: "🛠️ T-067 enforce branch_pr workflow in agentctl" }
comments:
  - { author: "CODER", body: "Implemented branch_pr enforcement + new commands; please run `python -m compileall scripts/agentctl.py` and spot-check `integrate --dry-run` output." }
  - { author: "INTEGRATOR", body: "Verified: merged commit 91b3760 on main; pr check and verify T-067 passed; handoff notes captured from PR review." }
description: "Implement the stricter branch_pr workflow spec: worktrees under .codex-swarm/worktrees, branch naming task/T-###/<slug>, new branch status, stricter pr open/update/check, integrate dry-run + verify in branch worktree, workflow_mode config in .codex-swarm/swarm.config.json, and stronger finish/guard/verify guardrails + standardized outputs."
---
