---
id: "202601041253-0002S"
title: "Refactor workflow paths"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["refactor", "paths"]
commit: { hash: "644b1fedd0789160916655344eb5ce49ed10f3e1", message: "✨ T-089 Move config + tasks paths" }
comments:
  - { author: "INTEGRATOR", body: "Verified: Not run (path refactor only); no runtime behavior changes; please run agentctl --help if needed." }
description: "Move agentctl into .codex-swarm and relocate workflow artifacts to .codex-swarm/workspace; update framework docs, agent prompts, and clean.sh to use the new paths while leaving historical task text unchanged."
dirty: false
redmine_id: 369
---
