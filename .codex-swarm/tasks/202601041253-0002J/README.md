---
id: "202601041253-0002J"
title: "Docs: update README and fix Mermaid diagram"
status: "DONE"
priority: "high"
owner: "PLANNER"
depends_on: ["202601041253-0002A", "202601041253-0002H"]
tags: ["docs", "workflow", "mermaid"]
verify: ["python scripts/agentctl.py task lint"]
commit: { hash: "c881605fdfef8585816e845648c826acf0c0ee6f", message: "🧪 T-082 refresh PR artifacts" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/T-082/pr." }
description: "Update root README.md to reflect latest branch_pr workflow and agentctl behavior (integrate auto-refresh artifacts; integrate may skip verify when SHA already verified). Fix Mermaid diagram so it renders correctly on GitHub."
---
