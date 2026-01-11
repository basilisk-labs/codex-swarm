---
id: "202601041253-00020"
title: "Restructure framework folders into .codex-swarm"
status: "DONE"
priority: "med"
owner: "CODER"
tags: ["framework", "refactor"]
verify: ["python scripts/agentctl.py task lint", "python scripts/agentctl.py agents", "python scripts/agentctl.py quickstart > /dev/null", "bash -n clean.sh"]
commit: { hash: "eb7cf5363ce55ec602fb9cc078069bc8d262a130", message: "Legacy completion (backfill)" }
comments:
  - { author: "REVIEWER", body: "Verified: Ran python scripts/agentctl.py verify T-064 (task lint, agents, quickstart, bash -n clean.sh); framework paths now live under .codex-swarm." }
description: "Move all framework-specific artifacts under .codex-swarm (agents + agentctl docs + config), update references/docs, and update clean.sh accordingly."
dirty: false
redmine_id: 344
---
