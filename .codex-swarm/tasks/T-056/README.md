---
id: "T-056"
title: "Add Mermaid agent workflow diagram to README"
status: "DONE"
priority: "med"
owner: "DOCS"
tags: ["docs", "workflow", "mermaid"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py agents"]
commit: { hash: "ebe53cd0a06d96bba5b1973375dbcbba2b65c917", message: "🧩 T-056 Add Mermaid workflow diagram" }
comments:
  - { author: "REVIEWER", body: "Verified: README now includes a Mermaid flowchart of the default agent workflow, reflecting current handoffs (CODER->TESTER, DOCS before finish) and the 3-phase commit cadence; agent registry and tasks lint pass." }
description: "Update @README.md to include a short description and a Mermaid diagram (flowchart) showing the default agent workflow and handoffs (ORCHESTRATOR, PLANNER, CODER, TESTER, DOCS, REVIEWER).\\n\\nAcceptance criteria:\\n- README includes a Mermaid flowchart block describing the typical flow (plan -> implement -> test -> docs -> review -> finish).\\n- Diagram matches current agent rules (3-phase commits, DOCS artifact before DONE, CODER -> TESTER for dev work)."
---
