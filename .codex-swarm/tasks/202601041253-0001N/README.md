---
id: "202601041253-0001N"
title: "Require DOCS workflow artifact before finishing tasks"
status: "DONE"
priority: "med"
owner: "CREATOR"
tags: ["agents", "docs", "workflow"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py agents"]
commit: { hash: "3fb0eb1971185bbd96efed13e037218cde291800", message: "🧾 T-053 Add workflow artifacts to DOCS" }
comments:
  - { author: "CREATOR", body: "Start: update DOCS to write docs/workflow/T-###.md artifacts and wire ORCHESTRATOR guidance to run DOCS before finishing tasks." }
  - { author: "REVIEWER", body: "Verified: DOCS now produces task-scoped workflow artifacts under docs/workflow/T-###.md before tasks are marked DONE, docs/workflow is present, and ORCHESTRATOR guidance schedules DOCS before finishing." }
description: "Change DOCS agent behavior so it runs before finishing any task and produces an atomic documentation artifact under @docs/workflow (e.g., @docs/workflow/T-025.md) describing what was implemented. Update orchestration guidance so plans include DOCS before REVIEWER marks tasks DONE.\\\\n\\\\nAcceptance criteria:\\\\n- @docs/workflow directory exists and is committed (with a short README describing artifact convention).\\\\n- @.AGENTS/DOCS.json instructs producing @docs/workflow/T-###.md artifacts (English, atomic, task-scoped).\\\\n- @AGENTS.md ORCHESTRATOR guidance schedules DOCS before finishing any task (DOCS before REVIEWER finish).\\\\n\\\\nNotes:\\\\n- Artifacts must be task-ID named, contain summary + changed files + verification commands (when available)."
---
