---
id: "202601041253-0002E"
title: "agentctl: pr check validates README completeness"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601041253-0002A"]
tags: ["agentctl", "workflow", "quality"]
verify: ["python -m compileall scripts/agentctl.py", "python scripts/agentctl.py task lint"]
commit: "1d665885edb4a478f1e627e75e0cceb8d34b569e"
comments:
  - { author: "INTEGRATOR", body: "Verified: Integrated via squash; verify=ran; pr=docs/workflow/T-078/pr." }
description: "Reduce review ping-pong by making `pr check` fail fast on placeholder docs.\\n\\nAcceptance:\\n- `python scripts/agentctl.py pr check T-123` validates `docs/workflow/T-123/README.md` exists and required sections are present and non-placeholder.\\n- Error message points to missing/empty section names.\\n- Supports legacy `docs/workflow/prs/T-123/description.md` during migration.\\n- Update `.codex-swarm/agentctl.md` to reflect the README-based PR doc."
dirty: false
redmine_id: 358
---
