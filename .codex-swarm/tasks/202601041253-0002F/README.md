---
id: "202601041253-0002F"
title: "Docs: remove remaining legacy prs/ mentions"
status: "DONE"
priority: "low"
owner: "DOCS"
depends_on: ["202601041253-0002A"]
tags: ["docs", "workflow"]
verify: ["python scripts/agentctl.py task lint"]
commit: { hash: "6b04b9b75b7c783b4beb33fac5d6a2fc3a95ce36", message: "🧾 T-079 remove legacy prs path mentions" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/T-079/pr." }
description: "Finish migration documentation cleanup.\\n\\nAcceptance:\\n- Update docs so they no longer instruct using `docs/workflow/prs/...` or `docs/workflow/T-###.md` (except clearly marked legacy notes).\\n- Includes at least: `docs/workflow/T-066/README.md`, `docs/workflow/T-067/README.md`, and any other references found via ripgrep.\\n- Do not rewrite historical task text in `tasks.json`; keep changes doc-only."
---
