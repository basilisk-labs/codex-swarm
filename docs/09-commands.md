# Commands Reference

## Quickstart
```bash
python .codex-swarm/agentctl.py quickstart
```

## Tasks
```bash
python .codex-swarm/agentctl.py task list
python .codex-swarm/agentctl.py task show 202601031816-7F3K2Q
python .codex-swarm/agentctl.py task add 202601031816-7F3K2Q --title "..." --description "..."
python .codex-swarm/agentctl.py task lint
python .codex-swarm/agentctl.py task export --format json --out .codex-swarm/tasks.json
```

## Branching and PR Artifacts
```bash
python .codex-swarm/agentctl.py branch create 202601031816-7F3K2Q --agent CODER --slug <slug> --worktree
python .codex-swarm/agentctl.py pr open 202601031816-7F3K2Q --branch task/202601031816-7F3K2Q/<slug> --author CODER
python .codex-swarm/agentctl.py pr update 202601031816-7F3K2Q
python .codex-swarm/agentctl.py pr check 202601031816-7F3K2Q
```

## Verification and Closure
```bash
python .codex-swarm/agentctl.py verify 202601031816-7F3K2Q
python .codex-swarm/agentctl.py finish 202601031816-7F3K2Q --commit <git-rev> --author INTEGRATOR --body "Verified: ..."
```
For batch finishes, include all task IDs in the commit subject, e.g. `✅ 202601031816-7F3K2Q 202601031817-1A9Z5C close ...`.

## Guardrails and Git Hygiene
```bash
python .codex-swarm/agentctl.py guard commit 202601031816-7F3K2Q -m "✨ 202601031816-7F3K2Q Summary" --allow <path>
git status --short
```

## Backend Sync (Redmine)
```bash
python .codex-swarm/agentctl.py sync redmine
python .codex-swarm/agentctl.py sync redmine --conflict=prefer-local
```

## Note
If `python` is not available, use `python3`.
