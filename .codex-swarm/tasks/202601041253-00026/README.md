---
id: "202601041253-00026"
title: "agentctl guard commit: add --auto-allow"
status: "DONE"
priority: "Нормальный"
owner: "Via Mentis Assistant"
depends_on: []
tags: []
verify: null
commit: "26eabcc06d63db1b67637df7bc84b849c27e789e"
comments: []
description: "Reduce commit friction by adding --auto-allow to python scripts/agentctl.py guard commit (same behavior as the commit wrapper): infer minimal --allow prefixes from staged files and run the same guard checks. Acceptance: (1) python scripts/agentctl.py guard commit T-### -m MSG --auto-allow works without explicit --allow; (2) keeps existing behavior when --allow is provided; (3) error messages remain actionable; (4) document in .codex-swarm/agentctl.md."
dirty: false
id_source: "custom"
redmine_id: 350
---
