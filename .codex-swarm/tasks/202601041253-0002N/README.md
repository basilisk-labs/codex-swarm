---
id: "202601041253-0002N"
title: "agentctl work start: idempotent scaffold"
status: "DONE"
priority: "Нормальный"
owner: "Via Mentis Assistant"
depends_on: []
tags: []
verify: null
commit: "e6d312e0b441b0deedf3c89c159fca9d9b4c09cb"
comments: []
description: "Fix python scripts/agentctl.py work start to be idempotent in branch_pr: if docs/workflow/T-###/README.md already exists in the new worktree (from the planning commit), do not fail or re-scaffold unless --overwrite is provided. This prevents frequent \\\"File already exists\\\" errors now that agents default to work start."
dirty: false
id_source: "custom"
redmine_id: 365
---
