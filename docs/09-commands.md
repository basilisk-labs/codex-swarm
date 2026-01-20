# Commands Reference

## Quickstart
```bash
python .codex-swarm/agentctl.py quickstart
```

## Config
```bash
python .codex-swarm/agentctl.py config show
python .codex-swarm/agentctl.py config set workflow_mode branch_pr
python .codex-swarm/agentctl.py config set tasks.verify.required_tags '["code","backend"]' --json
```

## Tasks
```bash
python .codex-swarm/agentctl.py task list
python .codex-swarm/agentctl.py task show 202601031816-7F3K2Q
python .codex-swarm/agentctl.py task new --title "..." --description "..." --priority med --owner CODER
python .codex-swarm/agentctl.py task add 202601031816-7F3K2Q --title "..." --description "..."
python .codex-swarm/agentctl.py task doc show 202601031816-7F3K2Q
python .codex-swarm/agentctl.py task doc set 202601031816-7F3K2Q --file .codex-swarm/tasks/202601031816-7F3K2Q/README.md
python .codex-swarm/agentctl.py task lint
# or run read-only commands with --lint
python .codex-swarm/agentctl.py task export --format json --out .codex-swarm/tasks.json
```

## Global flags

- `--quiet`: suppress non-essential output.
- `--verbose`: enable extra logging (when available).
- `--json`: emit JSON-formatted errors (for CI/integrations).
- `--lint`: force export lint at command start (useful for read-only commands).

## Recipes CLI
```bash
python .codex-swarm/recipes.py scan --recipes-dir .codex-swarm/recipes --output docs/recipes-inventory.json
python .codex-swarm/recipes.py show <slug> --json
python .codex-swarm/recipes.py compile <slug> --scenario <id> --inputs .codex-swarm/.runs/<run-id>/inputs.json --out .codex-swarm/.runs/<run-id>/bundle.json
python .codex-swarm/recipes.py explain <slug> --scenario <id> --inputs .codex-swarm/.runs/<run-id>/inputs.json
```
The scan output is the tracked recipe list at `docs/recipes-inventory.json`.

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
For batch finishes, include all task ID suffixes in the commit subject, e.g. `✅ 7F3K2Q 1A9Z5C close ...`.

## Guardrails and Git Hygiene
```bash
python .codex-swarm/agentctl.py guard commit 202601031816-7F3K2Q -m "✨ 202601031816-7F3K2Q Summary" --allow <path>
git status --short
```

## Optional Git Hooks
```bash
python .codex-swarm/agentctl.py hooks install
python .codex-swarm/agentctl.py hooks uninstall
```
Hooks are opt-in and enforce commit subjects with task suffixes plus protected-path and branch_pr pre-commit rules.

## Backend Sync (Redmine)
```bash
python .codex-swarm/agentctl.py sync redmine
python .codex-swarm/agentctl.py sync redmine --conflict=prefer-local
```

## Note
If `python` is not available, use `python3`.
