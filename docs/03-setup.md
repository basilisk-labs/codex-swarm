# Setup

## Clone and Open
```bash
git clone https://github.com/basilisk-labs/codex-swarm.git
cd codex-swarm
```
Open the repo in your IDE with the Codex plugin enabled.

## Optional Clean Slate
If you want a minimal snapshot for reuse, run:
```bash
./clean.sh
```
This removes framework-development artifacts and reinitializes git.

## Optional Virtual Environment
If you need extra Python packages for scripts:
```bash
python -m venv .venv
source .venv/bin/activate
pip install <package>
```
Install dependencies inside the venv only.

## Sanity Checks
- `python .codex-swarm/agentctl.py quickstart`
- `python .codex-swarm/agentctl.py task list`
- `python .codex-swarm/agentctl.py task lint` (or `--lint` on read-only commands)

## Backend Setup
1. Choose a backend plugin config in `.codex-swarm/backends/`.
2. Point `.codex-swarm/config.json` to that backend config (see `07-tasks-and-backends.md`).
3. For Redmine, validate API credentials and required custom fields.

## First Run
Start with the ORCHESTRATOR and describe your goal. It will propose a plan and ask for approval before any changes.

## Planned Expansions
- Add a copy-paste Redmine backend config example.
