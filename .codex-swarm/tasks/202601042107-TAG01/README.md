---
id: "202601042107-TAG01"
title: "Clarify planner task tags + deps"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["agents", "workflow"]
description: "Require PLANNER to review existing tags, apply the minimal set for navigation, and set dependencies when possible."
dirty: false
redmine_id: 277
---
# Summary

Clarify PLANNER instructions to always review existing tags, apply the minimal set for navigation, and set dependencies when possible when creating tasks.

# Scope

- Update PLANNER workflow guidance to enforce tag review/minimal tagging and dependency hints.

# Risks

- Low risk: guidance-only change; risk is limited to behavior alignment.

# Verify Steps

- None (documentation-only).

# Rollback Plan

- Revert the PLANNER instruction change if it causes confusion or conflicts with existing workflows.
