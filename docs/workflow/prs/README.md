# Local PR Artifacts (tracked)

This folder contains *tracked* PR-like artifacts used to review and integrate task branches locally (no GitHub/GitLab required).

## One task = one PR folder

For task `T-123`, keep artifacts under:

- `docs/workflow/prs/T-123/meta.json`
- `docs/workflow/prs/T-123/description.md` (must include: Summary / Scope / Risks / Verify / Rollback)
- `docs/workflow/prs/T-123/diffstat.txt`
- `docs/workflow/prs/T-123/verify.log`
- `docs/workflow/prs/T-123/review.md` (optional notes)

## Recommended commands

- Open: `python scripts/agentctl.py pr open T-123 --author CODER --branch task/T-123-<slug>`
- Update diffstat/meta: `python scripts/agentctl.py pr update T-123`
- Validate: `python scripts/agentctl.py pr check T-123`
- Integrate (INTEGRATOR on main): `python scripts/agentctl.py integrate T-123 --branch task/T-123-<slug> --merge-strategy squash --run-verify`

