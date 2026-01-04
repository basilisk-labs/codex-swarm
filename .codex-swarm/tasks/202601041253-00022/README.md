---
id: "202601041253-00022"
title: "Branch workflow: task branches + worktrees + local PR artifacts"
status: "DONE"
priority: "med"
owner: "ORCHESTRATOR"
tags: ["workflow", "git", "agentctl"]
verify: ["python scripts/agentctl.py task lint", "python -m compileall scripts/agentctl.py"]
commit: { hash: "9fd7273c23ae3490637588e158ff485627d93e4a", message: "🧩 T-066 add task-branch + worktree workflow" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Ran python scripts/agentctl.py task lint; python -m compileall scripts/agentctl.py; checked agentctl branch/pr/integrate help output." }
description: "Introduce a branching workflow to enable parallel agent work without tasks.json conflicts: task branch per T-###, required git worktree under .codex-swarm/worktrees, PR-like artifacts under docs/workflow/prs, and an INTEGRATOR role responsible for merge + finish on main."
dirty: false
redmine_id: 346
---
