# Agents

## Where Agents Live
All agents are defined in JSON under `.codex-swarm/agents/`. `AGENTS.md` provides the global rules that govern all of them.

## ORCHESTRATOR
- Starts every run.
- Translates a goal into a plan and requests approval.
- Coordinates handoffs between specialists.

## PLANNER
- Owns the task backlog.
- Uses agentctl to add/update tasks and enforce dependencies.
- Creates the initial per-task workflow artifact.

## CODER
- Implements changes with tight diffs.
- Runs local commands and summarizes key output.
- Hands off to TESTER and DOCS as needed.

## TESTER
- Adds or updates automated tests for changed behavior.
- Runs targeted tests and reports key results.
- Avoids introducing new frameworks unless requested.

## DOCS
- Updates user-facing documentation and task artifacts.
- Keeps docs aligned with current behavior.

## REVIEWER
- Reviews diffs and PR artifacts.
- Records findings by severity and suggests follow-ups.

## INTEGRATOR
- Merges task branches and closes tasks (required in `branch_pr`).
- Runs verify steps and updates PR artifacts on the base branch.

## CREATOR and UPDATER
- CREATOR adds new agents when no existing role fits the need.
- UPDATER audits and proposes improvements only when explicitly requested.
