# Commands Reference

## Quickstart
```bash
python .codex-swarm/agentctl.py quickstart
```

## Tasks
```bash
python .codex-swarm/agentctl.py task list
python .codex-swarm/agentctl.py task show T-123
python .codex-swarm/agentctl.py task add T-123 --title "..." --description "..."
python .codex-swarm/agentctl.py task lint
```

## Branching and PR Artifacts
```bash
python .codex-swarm/agentctl.py branch create T-123 --agent CODER --slug <slug> --worktree
python .codex-swarm/agentctl.py pr open T-123 --branch task/T-123/<slug> --author CODER
python .codex-swarm/agentctl.py pr update T-123
python .codex-swarm/agentctl.py pr check T-123
```

## Verification and Closure
```bash
python .codex-swarm/agentctl.py verify T-123
python .codex-swarm/agentctl.py finish T-123 --commit <git-rev> --author INTEGRATOR --body "Verified: ..."
```
For batch finishes, include all task IDs in the commit subject, e.g. `✅ T-123 T-124 close ...`.

## Guardrails and Git Hygiene
```bash
python .codex-swarm/agentctl.py guard commit T-123 -m "✨ T-123 Summary" --allow <path>
git status --short
```

## Note
If `python` is not available, use `python3`.
