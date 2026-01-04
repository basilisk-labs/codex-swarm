---
id: "202601041253-00029"
title: "Reduce integrate noise: auto-sync PR meta head_sha"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["agentctl", "workflow", "pipeline"]
verify: ["python -m compileall scripts/agentctl.py", "python scripts/agentctl.py task lint"]
commit: { hash: "6ee132fca0297c6909cdb6b2b60fa5e3f83bcc28", message: "✨ T-073 integrate meta head_sha sync" }
comments:
  - { author: "CODER", body: "Start: remove noisy integrate warning about stale PR meta head_sha by syncing to branch HEAD and correcting meta.json on main after merge; keep branch_pr safety. Verify via compileall + task lint and an integrate smoke." }
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/prs/T-073." }
description: "Speed up the pipeline by removing the common integrate warning about stale PR meta head_sha. Acceptance: (1) python scripts/agentctl.py integrate no longer prints \\\"PR meta head_sha differs\\\" in normal usage; (2) integrate uses the actual task branch HEAD SHA for verify and writes it into docs/workflow/prs/T-###/meta.json on main (head_sha + last_verified_sha) so artifacts stay consistent; (3) safe in workflow_mode=branch_pr and never writes to the task branch; (4) meta.json ends up correct after integration."
dirty: false
redmine_id: 353
---
