---
id: "T-081"
title: "agentctl integrate: skip verify if already verified"
status: "DONE"
priority: "high"
owner: "PLANNER"
depends_on: ["T-074"]
tags: ["agentctl", "workflow", "speed"]
verify: ["python -m compileall scripts/agentctl.py", "python scripts/agentctl.py task lint"]
commit: { hash: "0df88f39f6bb08d5fac2dabf5e113687135295a4", message: "🧪 T-081 refresh PR artifacts after verify" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/T-081/pr." }
description: "Speed up branch_pr integration by skipping redundant verify runs when the task branch HEAD SHA is already recorded as verified (via PR meta last_verified_sha or pr/verify.log). Keep --run-verify as a force-rerun escape hatch. Also ensure rebase strategy runs rebase before verify so the verified SHA matches what gets merged."
---
