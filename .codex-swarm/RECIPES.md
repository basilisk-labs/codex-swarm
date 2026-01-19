# Recipes: Global Prompt Rules

This document defines the global prompt conventions for recipe scenarios and compiled bundles in Codex Swarm.
It applies to all agents and the IDE integration that consume recipe bundles.

## Core rules

- Treat the compiled bundle (`bundle.json`) as the single source of truth.
- Never invent missing inputs or environment values. Missing data must surface as `Pending Actions`.
- Do not execute tools implicitly; tool execution is always an explicit, user-confirmed step.
- Do not read or write outside the allowlists defined by the recipe manifest and bundle policy.
- No network calls unless the manifest explicitly allows them (default: deny).
- Never write to `.codex-swarm/tasks/**` or `.codex-swarm/tasks.json`.

## Scenario prompts

Scenario Markdown is the canonical prompt for the workflow and should include:
- Required inputs (with defaults when applicable).
- Agents or roles involved.
- Context requirements (explicit file references).
- Steps and failure handling.
- Expected outputs (path templates).

If any required input is missing, output a `Pending Actions` section listing the missing fields.

## Bundle usage

When a bundle is provided:
- Use `compiled_prompt_md` verbatim as the execution prompt.
- Respect `tool_plan` for commands, working directories, and read/write allowlists.
- Use `context.files` entries for references, inline content, or snippets.
- Surface `env_missing` and `pending_actions` before any execution.

## Inputs and templating

Recipe templates use `<var>` placeholders for `slug`, `version`, and input keys.
For path templates:
- Sanitize values (no `..`, absolute paths, or `~`).
- If a variable is missing, keep `<var>` and add a pending action.

## Context policy

Context inclusion is controlled by the manifest policy:
- `include` and `exclude` define which files are eligible.
- Size and count limits must be enforced.
- Binary files are references only (no inline content).

Never expand context beyond the declared policy.

## Tool plan

The tool plan is a declaration, not execution:
- Confirm with the user or ORCHESTRATOR before running.
- Run from the declared `cwd`.
- Write outputs only to `writes_allowlist` locations.
- Report tool outputs and artifacts back to the ORCHESTRATOR.
