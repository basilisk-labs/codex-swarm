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
- `python .codex-swarm/agentctl.py task lint`

## First Run
Start with the ORCHESTRATOR and describe your goal. It will propose a plan and ask for approval before any changes.
