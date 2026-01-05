---
id: "202601041253-00021"
title: "Move architecture.md content into README"
status: "DONE"
priority: "med"
owner: "DOCS"
tags: ["docs", "refactor"]
verify: ["python scripts/agentctl.py task lint"]
commit: "6b22130b391becfada866dfc8136dbe1decff850"
comments:
  - { author: "REVIEWER", body: "Verified: Ran python scripts/agentctl.py verify T-065 (task lint) and reviewed README/architecture pointer consistency." }
description: "Move the full contents of docs/architecture.md into README.md for easier discovery; leave docs/architecture.md as a thin pointer to avoid duplication."
dirty: false
redmine_id: 345
---
