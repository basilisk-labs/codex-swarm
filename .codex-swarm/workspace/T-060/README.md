# T-060: Update agents to use agentctl docs + helpers

## Goal

Make the JSON agent workflows under `.codex-swarm/agents/` explicitly discover and follow the new agentctl documentation and helper commands.

## Scope

- Update `.codex-swarm/agents/*.json` to reference `.codex-swarm/agentctl.md` (via `python scripts/agentctl.py quickstart`).
- Prefer newly-added helpers where applicable:
  - `python scripts/agentctl.py task next|search|scaffold`
  - `python scripts/agentctl.py guard suggest-allow`
  - `python scripts/agentctl.py commit ...` (wrapper)

## Verification

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py agents`

## Implementation Notes

- Added an explicit first workflow step to the main specialist agents to run `python scripts/agentctl.py quickstart` and follow `.codex-swarm/agentctl.md`.
- Updated agent guidance to use the new helpers where relevant (scaffold, suggest-allow, commit wrapper).
