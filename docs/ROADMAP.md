# Roadmap

## Umbrella

- Task: 202601131125-20Z43B - Analyze config.json candidates.

## Epic 1: Inventory current configuration and usage

- Catalog current config keys and validation paths.
- Map hard-coded workflow settings across agentctl, docs, and agent prompts.
- Identify settings that behave like runtime toggles (often CLI flags).

## Epic 2: Propose config.json extensions + agentctl toggles

- Draft candidate config keys with defaults and scope (agent-facing vs tool-only).
- Flag which keys should be switchable via agentctl and which should be read-only.
- Note validation and backward-compatibility constraints.

## Epic 3: Optional follow-up implementation

- Outline migration steps and doc updates if changes are adopted.
- Define test/verify impact for agentctl changes.
