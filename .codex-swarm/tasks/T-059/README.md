---
id: "T-059"
title: "Add agentctl git/task ergonomics"
status: "DONE"
priority: "med"
owner: "CODER"
tags: ["agentctl", "git"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py guard --help"]
commit: { hash: "ba1828365b51d415ed3decea1053fd62060c34ff", message: "✨ T-059 Add agentctl ergonomics commands" }
comments:
  - { author: "REVIEWER", body: "Verified: Ran python scripts/agentctl.py task lint and python scripts/agentctl.py guard --help; spot-checked python scripts/agentctl.py task next and python scripts/agentctl.py task search agentctl." }
description: "Add higher-level CLI helpers: task next (ready tasks), task search, task scaffold (docs/workflow template), guard suggest-allow (derive minimal --allow set), and agentctl commit wrapper (guard + git commit)."
---
