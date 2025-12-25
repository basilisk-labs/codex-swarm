# T-058: Agentctl quickstart + docs pointer

## Goal

Make it faster for agents (and humans) to learn the `python scripts/agentctl.py` workflow by adding a focused usage cheat sheet and a CLI entrypoint that prints it.

## Scope

- Add `.codex-swarm/agentctl.md` with copy/paste examples.
- Add `python scripts/agentctl.py quickstart` (prints the cheat sheet / pointers).
- Link the doc from `AGENTS.md` (and optionally improve CLI help text).
- Update `clean.sh` to preserve `.codex-swarm/agentctl.md` while removing other `docs/` contents.

## Verification

- `python scripts/agentctl.py task lint`
- `python scripts/agentctl.py --help`
