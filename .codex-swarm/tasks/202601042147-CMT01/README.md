---
id: "202601042147-CMT01"
title: "Clarify commit message suffix usage"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["agents", "workflow"]
commit: { hash: "f1568e3460bd7e7a293bca7448b9e81348b8a575", message: "✨ CMT01 update agent commit message rule" }
comments:
  - { author: "INTEGRATOR", body: "Verified: not applicable (documentation-only); no tests or runtime behavior changed." }
description: "Require agents to use only the unique task index (suffix after the last dash) in commit messages, omitting the timestamp portion."
dirty: false
redmine_id: 278
---
# Summary

Clarified agent instructions so commit messages use only the unique task index (suffix after the last dash) and omit the timestamp portion.

# Scope

- Update agent workflow guidance to standardize commit message indexing.

# Risks

- Low risk: guidance-only change; impact is limited to commit message formatting.

# Verify Steps

- None (documentation-only).

# Rollback Plan

- Revert the agent instruction change if the commit naming convention needs to include timestamps again.
