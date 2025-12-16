# T-065: Move architecture.md content into README

## Goal

- Make architecture/workflow docs easier to discover by embedding them directly in `README.md`.

## Scope

- Copy the full contents of `docs/architecture.md` into `README.md` (new **Architecture & Workflow** section).
- Replace `docs/architecture.md` with a short pointer to the README section to avoid duplication while keeping links stable.

## Verification

- `python scripts/agentctl.py verify T-065`

## Notes

- Planning commit: `bddcf82` (🧭 T-065 plan move architecture into README)
- Implementation commit: `6b22130` (📝 T-065 embed architecture docs in README)
