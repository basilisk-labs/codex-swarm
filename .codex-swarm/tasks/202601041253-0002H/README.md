---
id: "202601041253-0002H"
title: "agentctl integrate: skip verify if already verified"
status: "DONE"
priority: "Нормальный"
owner: "Via Mentis Assistant"
depends_on: []
tags: []
verify: null
commit: "0df88f39f6bb08d5fac2dabf5e113687135295a4"
comments: []
description: "Speed up branch_pr integration by skipping redundant verify runs when the task branch HEAD SHA is already recorded as verified (via PR meta last_verified_sha or pr/verify.log). Keep --run-verify as a force-rerun escape hatch. Also ensure rebase strategy runs rebase before verify so the verified SHA matches what gets merged."
dirty: false
id_source: "custom"
redmine_id: 361
---
