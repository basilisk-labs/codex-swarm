---
id: "T-070"
title: "agentctl guard commit: add --auto-allow"
status: "DONE"
priority: "high"
owner: "CODER"
depends_on: ["T-068"]
tags: ["agentctl", "workflow", "pipeline"]
verify: ["python -m compileall scripts/agentctl.py", "python scripts/agentctl.py task lint"]
commit: { hash: "26eabcc06d63db1b67637df7bc84b849c27e789e", message: "✨ T-070 guard commit auto-allow" }
comments:
  - { author: "CODER", body: "Start: add --auto-allow to agentctl guard commit to infer allow prefixes from staged files; update .codex-swarm/agentctl.md; verify via compileall + task lint and a manual staged-change smoke." }
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/prs/T-070." }
description: "Reduce commit friction by adding --auto-allow to python scripts/agentctl.py guard commit (same behavior as the commit wrapper): infer minimal --allow prefixes from staged files and run the same guard checks. Acceptance: (1) python scripts/agentctl.py guard commit T-### -m MSG --auto-allow works without explicit --allow; (2) keeps existing behavior when --allow is provided; (3) error messages remain actionable; (4) document in .codex-swarm/agentctl.md."
---
