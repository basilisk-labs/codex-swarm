---
id: "202601041253-0001S"
title: "Fix Mermaid workflow diagram for GitHub rendering"
status: "DONE"
priority: "normal"
owner: "automation"
depends_on: []
tags: []
verify: null
commit: { hash: "13721c623fd186abbaee48456aa242f7e4561119", message: "Legacy completion (backfill)" }
comments: []
description: "Fix the Mermaid workflow diagram in @README.md so it renders correctly on GitHub (avoid problematic label characters like ### in node text).\\\\n\\\\nAcceptance criteria:\\\\n- Mermaid block renders on GitHub README view.\\\\n- Diagram still reflects current workflow (CODER->TESTER, DOCS before finish, 3-phase commits)."
dirty: false
id_source: "custom"
redmine_id: 337
---
