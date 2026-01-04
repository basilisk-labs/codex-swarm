# T-113: redmine backend: canonical source + offline fallback

## Summary

- Add a Redmine backend plugin with REST API integration.
- Implement offline fallback to the local cache and diff-based conflict handling.

## Goal

- Enable Redmine as a canonical backend while keeping local tasks as an offline cache.

## Scope

- Create `.codex-swarm/backends/redmine/backend.json` and `.codex-swarm/backends/redmine/backend.py`.
- Map Redmine issues to task frontmatter fields via custom fields.
- Implement `sync` with conflict strategies and offline fallback.

## Risks

- Redmine API constraints may require additional pagination or field mapping tweaks.
- Conflict handling is basic and may need refinement for complex field merges.

## Verify Steps

- `python3 -c "import importlib.util, pathlib; p=pathlib.Path('.codex-swarm/backends/redmine/backend.py'); s=importlib.util.spec_from_file_location('redmine_backend', p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.RedmineBackend)"`

## Rollback Plan

- Remove `.codex-swarm/backends/redmine/` and revert agentctl backend selection.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/backends/redmine/backend.json`: add Redmine backend plugin definition.
- `.codex-swarm/backends/redmine/backend.py`: add Redmine backend with offline fallback and sync.
<!-- END AUTO SUMMARY -->
