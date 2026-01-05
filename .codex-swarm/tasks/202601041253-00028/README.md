---
id: "202601041253-00028"
title: "agentctl task add: default depends_on to []"
status: "DONE"
priority: "normal"
owner: "Via Mentis Assistant"
depends_on: []
tags: []
verify: null
commit: "10b4ffcce3069a858b32580fe7247a1bb8a824a5"
comments: []
description: "Make the pipeline rule enforceable: update python scripts/agentctl.py task add to always write an explicit depends_on list (empty by default) so new tasks never omit the field. Also adjust AGENTS.md wording to clarify this requirement applies on task creation (legacy tasks may omit depends_on until updated)."
dirty: false
id_source: "custom"
redmine_id: 352
---
