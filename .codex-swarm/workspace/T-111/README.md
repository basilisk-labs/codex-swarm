# T-111: local backend: tasks/ storage + ID generation

## Summary

- Add a local backend plugin that reads/writes task frontmatter under `.codex-swarm/tasks/`.
- Provide basic frontmatter parsing/formatting and JSON snapshot export.

## Goal

- Establish a working local backend implementation to serve as the reference for backend routing and future sync behaviors.

## Scope

- Create `.codex-swarm/backends/local/backend.json` and `.codex-swarm/backends/local/backend.py`.
- Implement frontmatter parsing/formatting for core task fields.
- Implement local task listing, reading, writing, and JSON export.

## Risks

- Frontmatter parser is minimal and may not support complex YAML edge cases.
- Exported `tasks.json` lacks checksum metadata until later wiring.

## Verify Steps

- `python3 -c "import importlib.util, pathlib; p=pathlib.Path('.codex-swarm/backends/local/backend.py'); s=importlib.util.spec_from_file_location('local_backend', p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.LocalBackend)"`

## Rollback Plan

- Remove `.codex-swarm/backends/local/` and revert references to local backend.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/backends/local/backend.json`: add local backend plugin definition.
- `.codex-swarm/backends/local/backend.py`: add local backend implementation and frontmatter parsing helpers.
<!-- END AUTO SUMMARY -->
