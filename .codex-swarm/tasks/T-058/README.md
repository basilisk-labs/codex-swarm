---
id: "T-058"
title: "Agentctl quickstart + docs pointer"
status: "DONE"
priority: "med"
owner: "CODER"
tags: ["agentctl", "docs"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py --help"]
commit: { hash: "9bf8bdf414163bd3818b8d29075e19a4a87539ff", message: "✨ T-058 Add agentctl quickstart + docs" }
comments:
  - { author: "REVIEWER", body: "Verified: Ran agentctl lint and confirmed  prints ;  includes the new command; clean.sh preserves  while removing other docs." }
  - { author: "REVIEWER", body: "Verified: Ran python scripts/agentctl.py task lint; checked python scripts/agentctl.py quickstart output; checked python scripts/agentctl.py --help; confirmed clean.sh preserves docs/agentctl.md while removing other docs." }
description: "Add @docs/agentctl.md (usage cheat sheet), add agentctl quickstart command for printing it, and link from @AGENTS.md / CLI help so agents can learn the workflow faster."
---
