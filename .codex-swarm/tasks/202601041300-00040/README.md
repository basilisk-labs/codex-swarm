---
id: "202601041300-00040"
title: "tasks.html kanban viewer with local server"
status: "DONE"
priority: "med"
owner: "codex"
depends_on: []
tags: ["tasks-ui", "kanban"]
comments:
  - { author: "codex", body: "Started viewer/server refactor to move UI into .codex-swarm/viewer." }
description: "Build a local Python server module that serves tasks.html as a kanban board loaded from .codex-swarm/tasks.json with drag-and-drop status updates via backend, filters/sort/search, and light/dark themes."
---
# Summary

Build a local kanban viewer served by a single Python entrypoint, with drag-and-drop status updates backed by agentctl.

# Scope

- Move viewer assets into `.codex-swarm/viewer/`.
- Serve the viewer and `/api/tasks` from `.codex-swarm/viewer/tasks_server.py`.
- Support filters, sorting, search by title, and light/dark themes.
- Provide a Makefile flow for running and building a pywebview app.

# Risks

- pyinstaller packaging needs bundled viewer assets to render correctly.
- Drag-and-drop requires HTTP mode; file mode will be read-only.

# Verify Steps

- `./viewer.sh`
- Open `http://127.0.0.1:5179` and drag a card between columns.
- `make viewer-app` (after installing pywebview) to confirm app launch.

# Rollback Plan

- Revert the commit for this task.
