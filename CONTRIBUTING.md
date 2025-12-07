# Contributing to Codex Swarm

Thank you for your interest in contributing to **Codex Swarm**.
This document describes how we work on the project and how to propose changes.

---

## 0. TL;DR

- Small fixes (typos, docs, obvious bugs):
  → open a pull request from a feature branch, reference an issue if there is one.

- Any **global / architectural / behavioral change**:
  → **must start as an Issue**, be discussed and approved by maintainers,
  → only then implemented in a pull request.

---

## 1. Governance

- The project is maintained by the **Codex Swarm maintainers team**.
- Maintainers are responsible for:
  - reviewing and merging pull requests,
  - curating the roadmap and long-term architecture,
  - making final decisions in case of disagreement.

We aim for open discussion first, but maintainers have the final say to keep the
project coherent.

---

## 2. What counts as a “global change”

You **must open an Issue first** (design / proposal) for any change that:

- modifies the core agent orchestration or task model,
- changes public APIs, CLIs or configuration formats,
- impacts persistence (database schema, storage layout, on-disk formats),
- changes default behavior that existing users may rely on,
- introduces or replaces major dependencies or subsystems.

These Issues should:

1. Describe the problem and motivation.
2. Outline the proposed design (high-level, not full spec).
3. Discuss alternatives or trade-offs.
4. Include migration / backwards-compatibility notes if relevant.

Once maintainers agree on the direction, the Issue will be marked as **“approved for implementation”** and you (or someone else) can start a pull request.

---

## 3. Development workflow

1. **Fork the repository** (or create a feature branch if you have write access).
2. **Create a branch** from `main`:

```bash
git checkout -b feature/short-description
```

Implement your change, keeping commits logically separate and with clear
messages.

Run the tests / linters relevant for your change.
Check the project README for the current commands; if in doubt, at least run
whatever is available for local validation.

Update documentation if your change affects behavior, configuration or
public APIs.

Open a Pull Request:

- target branch: main,
- link the corresponding Issue (Closes #NNN),
- briefly describe what changed and why,
- mention any breaking changes or migration steps.

Address review comments from maintainers. When the PR is approved and CI is
green, a maintainer will merge it.

Direct commits to main are reserved for maintainers and automated tooling.

Task tracking follows the agent workflow: keep active items in branch-local `tasks-<branch>.json` files, avoid editing `tasks.json` on feature branches, and rely on the INTEGRATOR agent (on `main`) to import DONE tasks into `tasks.json` and regenerate `tasks.md` after merges.

4. Coding style
Follow the existing style in the files you modify.

Prefer clear, explicit code over clever one-liners.

Keep functions and modules focused; avoid mixing unrelated changes in one PR.

Add or update tests alongside new behavior whenever possible.

If you are unsure about style or structure, ask in the Issue before investing a
lot of time.

5. Documentation contributions
Improving documentation is highly appreciated:

- Fixing typos or unclear wording.
- Adding examples or usage notes.
- Clarifying configuration and deployment instructions.

Documentation changes also go through pull requests and should keep the
structure and tone of existing docs.

6. License and copyright
By contributing to Codex Swarm, you agree that:

- Your contributions are licensed under the same license as the project
  (currently MIT), and

- You have the right to provide the contribution under this license.

The project’s copyright notice must be preserved as described in LICENSE.
If you add files that originate from third-party sources, clearly mark their
license and provenance.

7. Code of Conduct
Please be respectful in all interactions in Issues, pull requests and other
project spaces.

A formal CODE_OF_CONDUCT.md may be added; until then, use common sense:
focus on technical arguments, assume good intent, and avoid personal attacks.
