---
id: "202601041253-00024"
title: "agentctl verify: log output + skip if unchanged"
status: "DONE"
priority: "med"
owner: "CODER"
tags: ["agentctl", "workflow", "pipeline"]
verify: ["python -m compileall scripts/agentctl.py", "python scripts/agentctl.py task lint"]
commit: "324e74e5f3bcb4ad1bb239eb1e02bac645553721"
comments:
  - { author: "CODER", body: "Start: Implement agentctl verify --log + --skip-if-unchanged; update PR meta.json with last_verified_sha/at and refresh .codex-swarm/agentctl.md. Plan: implement flags, add smoke steps, ensure branch_pr behavior. Risks: PR meta may be missing; keep safe fallbacks." }
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/prs/T-068." }
description: "Add flags to python scripts/agentctl.py verify to reduce manual PR bookkeeping and redundant runs. Acceptance: (1) verify T-### --log PATH appends a timestamped entry per verify command with combined stdout+stderr; (2) --skip-if-unchanged skips when current SHA (prefer PR meta.json head_sha when log path is under docs/workflow/prs/T-###, else git rev-parse HEAD in --cwd) matches last recorded verified SHA; (3) after success, record last_verified_sha and last_verified_at in PR meta.json when available; (4) document the new flow in .codex-swarm/agentctl.md."
dirty: false
redmine_id: 348
---
