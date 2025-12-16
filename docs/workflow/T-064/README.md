# T-064: Restructure framework folders into .codex-swarm

## Goal

- Move framework-specific files under `.codex-swarm/` (agents, CLI docs, config) while keeping project docs under `docs/`.

## Scope

- Migrate `.AGENTS/*.json` → `.codex-swarm/agents/*.json`.
- Move `docs/agentctl.md` → `.codex-swarm/agentctl.md`.
- Add `.codex-swarm/swarm-config.json` and make `scripts/agentctl.py` read its paths from there (no fallback to old paths).
- Update documentation and `clean.sh` to reflect the new structure.

## Verification

- `python scripts/agentctl.py verify T-064`

## Notes

- Planning commit: `4e99d5a` (🗂️ T-064 plan folder restructure)
- Implementation commit: `eb7cf53` (🧱 T-064 move framework into .codex-swarm)
- Follow-up: config was later consolidated/renamed to `.codex-swarm/swarm.config.json` (paths + workflow_mode).
