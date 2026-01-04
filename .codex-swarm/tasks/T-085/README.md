---
id: "T-085"
title: "agentctl work start: idempotent scaffold"
status: "DONE"
priority: "high"
owner: "CODER"
depends_on: ["T-075", "T-084"]
tags: ["agentctl", "workflow", "ergonomics"]
verify: ["python -m compileall scripts/agentctl.py", "python scripts/agentctl.py task lint"]
commit: { hash: "e6d312e0b441b0deedf3c89c159fca9d9b4c09cb", message: "🧾 T-085 refresh PR artifacts" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/T-085/pr." }
description: "Fix python scripts/agentctl.py work start to be idempotent in branch_pr: if docs/workflow/T-###/README.md already exists in the new worktree (from the planning commit), do not fail or re-scaffold unless --overwrite is provided. This prevents frequent \"File already exists\" errors now that agents default to work start."
---
