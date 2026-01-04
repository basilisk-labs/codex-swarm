---
id: "202601041253-0001S"
title: "Fix Mermaid workflow diagram for GitHub rendering"
status: "DONE"
priority: "med"
owner: "DOCS"
tags: ["docs", "mermaid", "workflow"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py agents"]
commit: { hash: "c7391edebc5a0ed392178ee311dba25cee93bf78", message: "🧬 T-057 Add detailed Mermaid sequence diagram" }
comments:
  - { author: "REVIEWER", body: "Verified: Mermaid flowchart + sequence diagram use GitHub-safe labels (no ###), diagram still reflects CODER->TESTER and DOCS pre-finish, and lint/agents checks pass." }
description: "Fix the Mermaid workflow diagram in @README.md so it renders correctly on GitHub (avoid problematic label characters like ### in node text).\\\\n\\\\nAcceptance criteria:\\\\n- Mermaid block renders on GitHub README view.\\\\n- Diagram still reflects current workflow (CODER->TESTER, DOCS before finish, 3-phase commits)."
---
