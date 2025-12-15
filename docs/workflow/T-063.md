# T-063: Redesign tasks.html (Codex Swarm) + dependency visualization

## Goal

- Make `tasks.html` feel simpler and lighter while branding it as **Codex Swarm**.
- Make task dependencies easy to understand at a glance (both upstream `depends_on` and downstream dependents).

## Scope

- Update the visual design (reduce visual noise, lighter surfaces, simpler typography).
- Add a dependency inspector panel driven by the current selection (URL hash / click).
- Show both:
  - Lists: upstream dependencies + downstream dependents (clickable).
  - Mini graph: an SVG “upstream → selected → downstream” visualization.
- Keep existing local-first loading behavior (auto-load `./tasks.json` over HTTP; file picker + drag/drop for `file://`).

## Verification

- `python scripts/agentctl.py task lint`
- Manual sanity check:
  - Open `tasks.html` and ensure tasks render.
  - Click a task id and confirm the dependency inspector updates.
  - Click an upstream/downstream item and confirm the selection changes and scrolls to that task.

## Implementation Notes

- Updated `tasks.html` visual design to be simpler and lighter; header is branded as Codex Swarm.
- Added a dependency inspector panel showing:
  - `blocked_by` (non-DONE upstream deps),
  - `depends_on` (upstream),
  - `dependents` (reverse deps),
  - and an SVG mini-graph for quick scanning.
- Commits:
  - Planning: `6d4f2141e7a3` (task + workflow artifact)
  - Implementation: `5e6efe85aa35` (UI + dependency map)
