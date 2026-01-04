---
id: "202601041253-00028"
title: "agentctl task add: default depends_on to []"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601041253-00027"]
tags: ["agentctl", "tasks", "dependencies"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py agents"]
commit: { hash: "10b4ffcce3069a858b32580fe7247a1bb8a824a5", message: "🛠️ T-072 default depends_on on task add" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/prs/T-072." }
description: "Make the pipeline rule enforceable: update python scripts/agentctl.py task add to always write an explicit depends_on list (empty by default) so new tasks never omit the field. Also adjust AGENTS.md wording to clarify this requirement applies on task creation (legacy tasks may omit depends_on until updated)."
---
