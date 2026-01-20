# feature-spec-to-tasks

This recipe turns a top-level task into a detailed implementation roadmap and task draft.
It writes the roadmap to `docs/roadmaps` and stores run artifacts under `.codex-swarm/.runs`.

## Outputs
- `docs/roadmaps/<roadmap_slug>.roadmap.md`
- `.codex-swarm/.runs/<run_id>/artifacts/<roadmap_slug>.plan.json`
- `.codex-swarm/.runs/<run_id>/artifacts/<roadmap_slug>.tasks.draft.md`
- (refactor-existing only) `.codex-swarm/.runs/<run_id>/artifacts/<roadmap_slug>.migration.md`

## Runner (local)
```bash
export RECIPE_INPUTS_PATH=.codex-swarm/.runs/<run-id>/inputs.json
export RECIPE_SCENARIO_ID=from-text
export RECIPE_RUN_ID=run-001
node .codex-swarm/recipes/feature-spec-to-tasks/tools/run-feature.js
```

Notes:
- The runner is deterministic and does not call the network.
- It overwrites roadmap outputs for the same slug/run id.
