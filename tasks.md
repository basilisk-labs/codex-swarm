# ✨ Project Tasks Board

_Last updated: 2025-11-28 18:08:26 UTC_

## **⭐ Summary**

| Icon | Metric | Count |
| --- | --- | --- |
| 🧮 | **Total** | 47 |
| 📋 | **Backlog** | 0 |
| 🚧 | **In Progress** | 0 |
| ⛔ | **Blocked** | 0 |
| ✅ | **Done** | 47 |

🌈 **Palette note:** Keep `python scripts/tasks.py` handy so the table stays in sync after every update.
🎉 **Vibe check:** Emoji commits + clear summaries = joyful collaborators.

## **📋 Backlog**
_No open tasks._

## **🚧 In Progress**
_No active tasks._

## **⛔ Blocked**
_No blocked tasks._

## **✅ Done**
- ✅ **[T-001] Document framework in README**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `readme`
  - **Description:** Summarize the overall multi-agent workflow so newcomers can understand the repository quickly.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-002] Restructure agent registry into JSON files**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `agents`, `architecture`
  - **Description:** Split every reusable agent prompt into a dedicated JSON file under .AGENTS for easier maintenance.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-003] Move tasks data into .AGENTS/TASKS.json**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `state`, `persistence`
  - **Description:** Ensure task state is available in a machine-readable JSON file for Codex automation.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-004] Enforce per-task git commits in AGENTS spec**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `workflow`, `agents`
  - **Description:** Document the rule that every plan item must end with its own git commit for traceability.
  - **_Commit:_** [`fb9f40f`](https://github.com/basilisk-labs/codex-swarm/commit/fb9f40ff9b294361cf2d6322d4b68d220ebbf1c6) — T-004: enforce per-task commits
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-005] Document commit workflow in README**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `workflow`
  - **Description:** Expand the README with details on emoji commits and atomic task tracking.
  - **_Commit:_** [`fa8627b`](https://github.com/basilisk-labs/codex-swarm/commit/fa8627b7e1cb31047987216d42f6664cd1fe8767) — T-005: document commit workflow
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-006] Add Agent Creator workflow**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `agents`, `automation`
  - **Description:** Describe how new specialist agents are proposed, reviewed, and added to the registry.
  - **_Commit:_** [`3a9cc7d`](https://github.com/basilisk-labs/codex-swarm/commit/3a9cc7dcbf8d8ada931d5318ce04ed855254888c) — Mark T-006 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-007] Improve commit message guidance**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `workflow`, `git`
  - **Description:** Tighten the instructions around writing meaningful, emoji-prefixed commit messages.
  - **_Commit:_** [`6e8c80e`](https://github.com/basilisk-labs/codex-swarm/commit/6e8c80e12a6127ec040d1148cee1bfe1e0e41772) — Mark T-007 and T-008 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-008] Document repository structure in README**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `readme`
  - **Description:** Add a quick-start tour of key files and directories so contributors know where to work.
  - **_Commit:_** [`6e8c80e`](https://github.com/basilisk-labs/codex-swarm/commit/6e8c80e12a6127ec040d1148cee1bfe1e0e41772) — Mark T-007 and T-008 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-009] Define status transition protocol**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `workflow`, `tasks`
  - **Description:** Clarify which agent owns each state change and how statuses move between TODO/DOING/DONE/BLOCKED.
  - **_Commit:_** [`bb1d029`](https://github.com/basilisk-labs/codex-swarm/commit/bb1d0296309f47bcfe7b541b9157a92306cb8543) — Mark T-009 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-010] Automate agent registry updates**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `agents`, `automation`
  - **Description:** Explain how the orchestrator scans .AGENTS/*.json dynamically instead of relying on a manual list.
  - **_Commit:_** [`0b4a14c`](https://github.com/basilisk-labs/codex-swarm/commit/0b4a14ca3a4c48f4c19dee823103cb927dcae2f1) — Mark T-010 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-011] Evaluate workflow and suggest improvements**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `workflow`, `analysis`
  - **Description:** Review the end-to-end authoring flow and capture improvement ideas inside the docs.
  - **_Commit:_** [`d9572ab`](https://github.com/basilisk-labs/codex-swarm/commit/d9572ab9f3738eced63f4d13f9d149d1d6af6517) — Docs T-011 workflow analysis
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-012] Generalize AGENTS.md to remove agent-specific guidance**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `agents`
  - **Description:** Keep AGENTS.md focused on cross-agent protocol instead of baking in individual instructions.
  - **_Commit:_** [`e92c420`](https://github.com/basilisk-labs/codex-swarm/commit/e92c42039af7d566e79e2d7651c718e1fdaa8b88) — Review T-012 generalize AGENTS spec
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-013] Align agent prompts with GPT-5.1 guide**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `prompting`, `agents`
  - **Description:** Update every agent spec so prompts match the GPT-5.1 best practices.
  - **_Commit:_** [`a70b131`](https://github.com/basilisk-labs/codex-swarm/commit/a70b1319af38ab8f8cc3d04d002a01aa4ef70e92) — Mark T-013 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-014] Document Cursor + Codex local workflow in AGENTS.md**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `agents`
  - **Description:** Add environment assumptions for local-only workflows without remote runtimes.
  - **_Commit:_** [`db89025`](https://github.com/basilisk-labs/codex-swarm/commit/db8902599b40ae42ed97c009f1c17e3402664783) — Mark T-014 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-015] Align agent prompts with Cursor + Codex constraints**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `prompting`, `agents`
  - **Description:** Ensure prompts mention the IDE limitations so agents avoid referencing unavailable tools.
  - **_Commit:_** [`9358629`](https://github.com/basilisk-labs/codex-swarm/commit/9358629edcbdb575b58a9903e647d765b5dfe03f) — Mark T-015 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-016] Remove tool references from AGENTS.md for Codex-only workflow**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `agents`
  - **Description:** Strip references to unsupported helper tools to keep instructions aligned with the local stack.
  - **_Commit:_** [`d5b3e2e`](https://github.com/basilisk-labs/codex-swarm/commit/d5b3e2eac2dc04098d97248ddba1dcca271311fa) — Mark T-016 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-017] Update agent prompts for tool-less Codex context**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `prompting`, `agents`
  - **Description:** Reword prompts so agents do not assume access to external search or commands.
  - **_Commit:_** [`6ed438a`](https://github.com/basilisk-labs/codex-swarm/commit/6ed438a36b77e1ae7ca742ce4ace0fd4391c978e) — Mark T-017 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-018] Streamline AGENTS.md English guidelines**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `agents`
  - **Description:** Trim redundant English-language instructions and keep the doc crisp.
  - **_Commit:_** [`673ff98`](https://github.com/basilisk-labs/codex-swarm/commit/673ff98d3b5efdba4cf81a4ce4b5558748d8ed3e) — Mark T-018 complete
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-019] Add glossary-aware translation agent**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `agents`, `localization`
  - **Description:** Introduce a translator agent that respects glossary entries when localizing README content.
  - **_Commit:_** [`4cf2f07`](https://github.com/basilisk-labs/codex-swarm/commit/4cf2f07b1c9c8dddeb76cd85aa9cdff07cf4bb07) — Add T-019 translator agent
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-020] Add Spanish README translation**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `localization`
  - **Description:** Provide a Spanish version of the README while keeping glossary terms consistent.
  - **_Commit:_** [`631c837`](https://github.com/basilisk-labs/codex-swarm/commit/631c837f044c2f8ff5a3a785cca6d695a990b3a2) — Mark T-020 done after README.es review
  - 💬 **Comments:**
    - **reviewer:** _Added README.es.md and ensured glossary coverage for Spanish terminology._

- ✅ **[T-021] Enhance translator glossary workflow**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `agents`, `localization`
  - **Description:** Teach the translator agent how to maintain glossary metadata and usage counts automatically.
  - **_Commit:_** [`e19258d`](https://github.com/basilisk-labs/codex-swarm/commit/e19258da08620b2b494932ebaa96c806ada33699) — Mark T-021 done
  - 💬 **Comments:**
    - **reviewer:** _Updated the TRANSLATOR agent so every run maintains GLOSSARY.json, tracks usage frequencies, and enforces approved terms._

- ✅ **[T-022] Add Russian README translation**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `localization`
  - **Description:** Add a Russian localization of the README plus supporting glossary entries.
  - **_Commit:_** [`934d327`](https://github.com/basilisk-labs/codex-swarm/commit/934d327f0938d4b76760cb585073b6d69b223e6d) — Mark T-022 done after translation review
  - 💬 **Comments:**
    - **reviewer:** _Added README.ru.md plus GLOSSARY.json context so translation terminology stays consistent._

- ✅ **[T-023] Add Spanish README translation**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `localization`
  - **Description:** Deliver another Spanish README update incorporating the refined glossary process.
  - **_Commit:_** [`1f58561`](https://github.com/basilisk-labs/codex-swarm/commit/1f58561634734d0e73374ccd1264d15d57f7c251) — T-023: mark Spanish README translation done
  - 💬 **Comments:**
    - **reviewer:** _Created README.es.md and updated GLOSSARY.json with Spanish equivalents for existing terms._

- ✅ **[T-024] Revise glossary schema for translations**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `localization`, `glossary`
  - **Description:** Restructure the glossary so English remains canonical while localized entries store metadata per language.
  - **_Commit:_** [`eb5a185`](https://github.com/basilisk-labs/codex-swarm/commit/eb5a18530947e3387e401f9539595db257492b0c) — T-024: finalize glossary schema work
  - 💬 **Comments:**
    - **reviewer:** _Updated the TRANSLATOR workflow and converted GLOSSARY.json so languages own their preferred terms and descriptions._

- ✅ **[T-025] Clarify emoji commit workflow**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `workflow`, `git`
  - **Description:** Clarify how commits should start with emojis and summarize completed plan items.
  - **_Commit:_** [`8b9cb04`](https://github.com/basilisk-labs/codex-swarm/commit/8b9cb04780d1d21ba8016303cbb79754c5931b94) — ✅ Mark T-025 done
  - 💬 **Comments:**
    - **reviewer:** _Updated AGENTS.md and README.md so commit messages start with meaningful emojis referencing the finished plan item._

- ✅ **[T-026] Enforce atomic task planning**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `workflow`, `planning`
  - **Description:** Ensure the PLANNER splits every request into single-owner tasks with unique commits.
  - **_Commit:_** [`851c576`](https://github.com/basilisk-labs/codex-swarm/commit/851c576b97b52541b3cab13ed3555c97d4d1f475) — 🧩 T-026 enforce atomic planning
  - 💬 **Comments:**
    - **reviewer:** _Updated .AGENTS/PLANNER.json, AGENTS.md, and README.md so the PLANNER keeps tasks atomic._

- ✅ **[T-027] Add UPDATER optimization agent**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `agents`, `optimization`
  - **Description:** Introduce an agent dedicated to auditing the repository and proposing optimizations to existing agents when explicitly requested.
  - **_Commit:_** [`1f484b2`](https://github.com/basilisk-labs/codex-swarm/commit/1f484b210e0b3c5f94db94ab08d846bb9661035f) — ✅ Review UPDATER agent deliverable (T-027)
  - 💬 **Comments:**
    - **reviewer:** _Verified .AGENTS/UPDATER.json and AGENTS.md to ensure the new agent only runs on explicit optimization requests and outputs a repo-wide optimization plan._

- ✅ **[T-028] Add virtualenv installation reminder**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `workflow`
  - **Description:** Add a global reminder that any external libraries required by scripts must be installed only inside virtual environments.
  - **_Commit:_** [`cc7a020`](https://github.com/basilisk-labs/codex-swarm/commit/cc7a02002b47e16d7d7b6cea5a5d8a935cbdb54d) — ✅ mark T-028 done
  - 💬 **Comments:**
    - **docs:** _Added AGENTS.md guidance reminding contributors to install external dependencies only within virtual environments before running scripts._

- ✅ **[T-029] Audit agents for optimization opportunities**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🔍 UPDATER` • **Tags:** `agents`, `optimization`
  - **Description:** Review every agent prompt and workflow the user asked about to find practical optimizations and recommend next steps.
  - **_Commit:_** [`32b4219`](https://github.com/basilisk-labs/codex-swarm/commit/32b4219cc283f233a1b2d68a6ea9d86a2e65a12d) — 🧭 T-029 finish agent audit
  - 💬 **Comments:**
    - **UPDATER:** _Reported the missing glossary and CODER permission gaps plus suggested focused follow-ups._

- ✅ **[T-030] Clarify CODER agent permissions**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🛠️ CODER` • **Tags:** `agents`, `permissions`
  - **Description:** Align the CODER role with actual responsibilities by expanding permissions and workflow details per the recent request.
  - **_Commit:_** [`c7f224c`](https://github.com/basilisk-labs/codex-swarm/commit/c7f224ce23c0a0b2e46ab6e5d03858a8faea7295) — 🧩 T-030 revise coder agent
  - 💬 **Comments:**
    - **CODER:** _Expanded permissions, workflow detail, and verification guidance to match the current responsibilities._

- ✅ **[T-031] Sync README with current agent lineup**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `readme`
  - **Description:** Refresh README.md so it describes the existing agents (including UPDATER), workflow rules, and repository layout that reflect the latest codebase.
  - **_Commit:_** [`08a0c4b`](https://github.com/basilisk-labs/codex-swarm/commit/08a0c4b4451bafc5e8b75bf1b4a8f4c74594dc05) — ✅ T-031 finish README sync task
  - 💬 **Comments:**
    - **docs:** _README now mentions the UPDATER optimization agent and lifecycle so the doc mirrors the current codebase._

- ✅ **[T-032] Stylize README with icons and ASCII art**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `readme`
  - **Description:** Enhance README.md by introducing inline icons, refined formatting, and an ASCII-art title while keeping the workflow explanation intact.
  - **_Commit:_** [`f6eecde`](https://github.com/basilisk-labs/codex-swarm/commit/f6eecde89e99f7a3c31413e3a173620bd64331c9) — 📝 T-032 stylize README
  - 💬 **Comments:**
    - **docs:** _README now shows ASCII art, icons, and refreshed formatting so it feels more polished._

- ✅ **[T-033] Style tasks board markdown output**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `workflow`, `formatting`
  - **Description:** Bold every heading, wrap Priority/Owner/Tags values in code spans, display agent names uppercase with icons, and turn commit hashes into GitHub links on the generated board.
  - **_Commit:_** [`2f93325`](https://github.com/basilisk-labs/codex-swarm/commit/2f93325a23837b89b0431b3219cee725b6902583) — 🛠️ T-033 style tasks board
  - 💬 **Comments:**
    - **reviewer:** _Verified the board now bolds headings, code-highlights metadata, uppercases agent owners with icons, and links commit hashes._

- ✅ **[T-034] Bold status, description, commit labels**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `workflow`, `formatting`
  - **Description:** Render the `_Status`, `_Description`, and `_Commit` prefixes as bold text while leaving their italic suffixes intact.
  - **_Commit:_** [`f520084`](https://github.com/basilisk-labs/codex-swarm/commit/f52008459f7415f33a7d3064d064ec841718d00e) — 🛠️ T-034 bold label headers
  - 💬 **Comments:**
    - **reviewer:** _Confirmed the label prefixes are bold while the italics remain on the suffix, so the board matches the request._

- ✅ **[T-035] Remove italic on description label**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `workflow`
  - **Description:** Render the description label without italics so only the bold text shows.
  - **_Commit:_** [`6c5bc66`](https://github.com/basilisk-labs/codex-swarm/commit/6c5bc662a3f71b8e206a48133cc401033142ccd2) — 🛠️ T-035 remove description italic
  - 💬 **Comments:**
    - **reviewer:** _Confirmed the description label is no longer italicized yet still stands out via bold styling._

- ✅ **[T-036] Beautify summary table**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🤖 CODEX` • **Tags:** `docs`, `workflow`, `formatting`
  - **Description:** Turn the summary list into an emoji-rich table and add extra decorative flair, keeping the `_Status` italic values as-is.
  - **_Commit:_** [`463a885`](https://github.com/basilisk-labs/codex-swarm/commit/463a8853f38d3b9f3ebd9f6a191f3f7c81db0aa7) — 🛠️ T-036 beautify summary table
  - 💬 **Comments:**
    - **reviewer:** _Confirmed the summary section is now a table with playful emoji notes and the `_Status` italic text stays intact._

- ✅ **[T-037] Add CONTRIBUTING guidelines**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `workflow`
  - **Description:** Document the recommended contribution workflow and behavioral expectations for Codex Swarm.
  - **_Commit:_** [`ec13d91`](https://github.com/basilisk-labs/codex-swarm/commit/ec13d916bfc5d0e577b757d2a16dd8380ca3861d) — 📝 T-037 add contributing guidelines
  - 💬 **Comments:**
    - **docs:** _Added CONTRIBUTING.md with the requested contribution guidance._

- ✅ **[T-038] Document README usage guidance**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `readme`
  - **Description:** Ensure README describes the codebase and includes local development steps (download Zip, run clean.sh).
  - **_Commit:_** [`bec7e7d`](https://github.com/basilisk-labs/codex-swarm/commit/bec7e7de9cbeaed166adefb51ff2c497e1ffa1fc) — 📝 T-038 update README local dev
  - 💬 **Comments:**
    - **docs:** _Extended README with code breakdown and local dev steps (download zip, run clean.sh)._

- ✅ **[T-039] Update cleanup script to remove CONTRIBUTING.md and itself**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🧠 HUMAN` • **Tags:** `automation`, `cleanup`
  - **Description:** Adjust clean.sh so it also deletes CONTRIBUTING.md and cleans itself up after resetting the repo.
  - **_Commit:_** [`25d2b91`](https://github.com/basilisk-labs/codex-swarm/commit/25d2b916ec4f2fbdf3caa0553c6271974acffdab) — 🛠️ T-039 update cleanup script to remove CONTRIBUTING.md and self
  - 💬 **Comments:**
    - **docs:** _clean.sh now removes CONTRIBUTING.md and deletes itself after repository cleanup._

- ✅ **[T-040] Add README onboarding sections**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `readme`
  - **Description:** Add a focused Getting Started path, example session log, and limitations/non-goals to README with a simpler intro.
  - **_Commit:_** [`f9c3e6c`](https://github.com/basilisk-labs/codex-swarm/commit/f9c3e6c1e4bb906895811443799ef70faf18c7a3) — 📘 T-040 add README onboarding
  - 💬 **Comments:**
    - **docs:** _Refreshed README intro, added a concrete Getting Started path with clean.sh guidance, an example session, and a Limitations/Non-goals section._

- ✅ **[T-041] Document framework guideline**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `guideline`
  - **Description:** Create GUIDELINE.md that explains prerequisites, setup, installation, and step-by-step usage of the Codex Swarm framework.
  - **_Commit:_** [`21ddede`](https://github.com/basilisk-labs/codex-swarm/commit/21ddede356590745546962fedebbead23b2edae2) — 📝 T-041 document framework guideline
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-042] Expand framework guideline**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `guideline`, `workflow`
  - **Description:** Add example sessions, troubleshooting tips, and best practices to GUIDELINE.md so the framework flow is crystal clear.
  - **_Commit:_** [`18a62ee`](https://github.com/basilisk-labs/codex-swarm/commit/18a62ee44d660dd7d7e8590329edb92194e4eba6) — 📝 T-042 expand framework guideline
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-043] Update .gitignore to include .env files**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `🧠 HUMAN` • **Tags:** `git`, `workflow`
  - **Description:** Ignore `.env*` so sensitive environment overrides stay out of the repo.
  - **_Commit:_** [`a63694f`](https://github.com/basilisk-labs/codex-swarm/commit/a63694f182aff97ce18b5b9458bf54982e787120) — 🛠️ T-043 update .gitignore to include .env files
  - 💬 **Comments:**
    - **docs:** _.gitignore now ignores `.env` variants following the cleanup._

- ✅ **[T-044] Add sync_tasks.py script to synchronize tasks.json with GitHub Issues**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🧠 HUMAN` • **Tags:** `automation`, `sync`
  - **Description:** Ensure the local tasks.json reflects the completed synchronization script and the GitHub Issues mirror.
  - **_Commit:_** [`5e3b74a`](https://github.com/basilisk-labs/codex-swarm/commit/5e3b74a497ada1b723813b416747ccc47ca6ddbc) — ✨ T-044 add sync_tasks.py script to synchronize tasks.json with GitHub Issues
  - 💬 **Comments:**
    - **docs:** _Recorded completion of sync_tasks.py so tasks.json stays aligned with GitHub Issues._

- ✅ **[T-045] Add GitHub Actions workflow to sync tasks.json with GitHub Issues**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🧠 HUMAN` • **Tags:** `automation`, `workflow`
  - **Description:** Document the new `.github/workflows/sync-tasks.yml` workflow that keeps tasks.json and GitHub Issues synchronized.
  - **_Commit:_** [`7b8445b`](https://github.com/basilisk-labs/codex-swarm/commit/7b8445b4326e1d8c52e7f0e2718b9d88f75db502) — ✨ T-045 add GitHub Actions workflow to sync tasks.json with GitHub Issues
  - 💬 **Comments:**
    - **docs:** _Workflow file exists and ensures tasks.json is kept in sync via GitHub Actions._

- ✅ **[T-046] Enhance sync_tasks.py to integrate ProjectV2 status updates and project number**
  - **_Status:_** *Done*
  - **Priority:** `high` • **Owner:** `🧠 HUMAN` • **Tags:** `automation`, `project`, `sync`
  - **Description:** The sync_tasks.py script now updates ProjectV2 items' Status fields and the workflow passes the project number; record this completion.
  - **_Commit:_** [`ef12528`](https://github.com/basilisk-labs/codex-swarm/commit/ef12528c6ce74b53ca93b8f83a872ede49b81e26) — ✨ T-046 enhance sync_tasks.py to integrate ProjectV2 status updates and update workflow with project number
  - 💬 **Comments:**
    - **docs:** _ProjectV2 integration is wired up, and the workflow now provides the project number._

- ✅ **[T-047] Create Code of Conduct**
  - **_Status:_** *Done*
  - **Priority:** `med` • **Owner:** `📚 DOCS` • **Tags:** `docs`, `policy`
  - **Description:** Write a Code of Conduct that outlines expected community behavior, reporting channels, and enforcement principles.
  - **_Commit:_** [`113c748`](https://github.com/basilisk-labs/codex-swarm/commit/113c748a1f5c9bd56bc96ccb5616930310f7776d) — 📌 T-047 start Code of Conduct task
  - 💬 **Comments:**
    - **docs:** _Added CODE_OF_CONDUCT.md covering standards, unacceptable behaviors, and reporting guidance._
