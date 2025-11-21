# ✨ Project Tasks Board

_Last updated: 2025-11-21 17:32:28 UTC_

## ⭐ Summary
- 🧮 **Total:** 32
- 📋 **Backlog:** 0
- 🚧 **In Progress:** 0
- ⛔ **Blocked:** 0
- ✅ **Done:** 32

## 📋 Backlog
_No open tasks._

## 🚧 In Progress
_No active tasks._

## ⛔ Blocked
_No blocked tasks._

## ✅ Done
- ✅ **[T-001] Document framework in README**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, readme
  - _Description:_ Summarize the overall multi-agent workflow so newcomers can understand the repository quickly.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-002] Restructure agent registry into JSON files**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, architecture
  - _Description:_ Split every reusable agent prompt into a dedicated JSON file under .AGENTS for easier maintenance.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-003] Move tasks data into .AGENTS/TASKS.json**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** state, persistence
  - _Description:_ Ensure task state is available in a machine-readable JSON file for Codex automation.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-004] Enforce per-task git commits in AGENTS spec**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, agents
  - _Description:_ Document the rule that every plan item must end with its own git commit for traceability.
  - _Commit:_ `fb9f40f` — T-004: enforce per-task commits
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-005] Document commit workflow in README**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, workflow
  - _Description:_ Expand the README with details on emoji commits and atomic task tracking.
  - _Commit:_ `fa8627b` — T-005: document commit workflow
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-006] Add Agent Creator workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, automation
  - _Description:_ Describe how new specialist agents are proposed, reviewed, and added to the registry.
  - _Commit:_ `3a9cc7d` — Mark T-006 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-007] Improve commit message guidance**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, git
  - _Description:_ Tighten the instructions around writing meaningful, emoji-prefixed commit messages.
  - _Commit:_ `6e8c80e` — Mark T-007 and T-008 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-008] Document repository structure in README**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, readme
  - _Description:_ Add a quick-start tour of key files and directories so contributors know where to work.
  - _Commit:_ `6e8c80e` — Mark T-007 and T-008 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-009] Define status transition protocol**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, tasks
  - _Description:_ Clarify which agent owns each state change and how statuses move between TODO/DOING/DONE/BLOCKED.
  - _Commit:_ `bb1d029` — Mark T-009 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-010] Automate agent registry updates**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** agents, automation
  - _Description:_ Explain how the orchestrator scans .AGENTS/*.json dynamically instead of relying on a manual list.
  - _Commit:_ `0b4a14c` — Mark T-010 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-011] Evaluate workflow and suggest improvements**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** workflow, analysis
  - _Description:_ Review the end-to-end authoring flow and capture improvement ideas inside the docs.
  - _Commit:_ `d9572ab` — Docs T-011 workflow analysis
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-012] Generalize AGENTS.md to remove agent-specific guidance**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Keep AGENTS.md focused on cross-agent protocol instead of baking in individual instructions.
  - _Commit:_ `e92c420` — Review T-012 generalize AGENTS spec
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-013] Align agent prompts with GPT-5.1 guide**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** prompting, agents
  - _Description:_ Update every agent spec so prompts match the GPT-5.1 best practices.
  - _Commit:_ `a70b131` — Mark T-013 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-014] Document Cursor + Codex local workflow in AGENTS.md**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Add environment assumptions for local-only workflows without remote runtimes.
  - _Commit:_ `db89025` — Mark T-014 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-015] Align agent prompts with Cursor + Codex constraints**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** prompting, agents
  - _Description:_ Ensure prompts mention the IDE limitations so agents avoid referencing unavailable tools.
  - _Commit:_ `9358629` — Mark T-015 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-016] Remove tool references from AGENTS.md for Codex-only workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Strip references to unsupported helper tools to keep instructions aligned with the local stack.
  - _Commit:_ `d5b3e2e` — Mark T-016 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-017] Update agent prompts for tool-less Codex context**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** prompting, agents
  - _Description:_ Reword prompts so agents do not assume access to external search or commands.
  - _Commit:_ `6ed438a` — Mark T-017 done
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-018] Streamline AGENTS.md English guidelines**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Trim redundant English-language instructions and keep the doc crisp.
  - _Commit:_ `673ff98` — Mark T-018 complete
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-019] Add glossary-aware translation agent**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, localization
  - _Description:_ Introduce a translator agent that respects glossary entries when localizing README content.
  - _Commit:_ `4cf2f07` — Add T-019 translator agent
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-020] Add Spanish README translation**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, localization
  - _Description:_ Provide a Spanish version of the README while keeping glossary terms consistent.
  - _Commit:_ `631c837` — Mark T-020 done after README.es review
  - 💬 **Comments:**
    - **reviewer:** _Added README.es.md and ensured glossary coverage for Spanish terminology._

- ✅ **[T-021] Enhance translator glossary workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, localization
  - _Description:_ Teach the translator agent how to maintain glossary metadata and usage counts automatically.
  - _Commit:_ `e19258d` — Mark T-021 done
  - 💬 **Comments:**
    - **reviewer:** _Updated the TRANSLATOR agent so every run maintains GLOSSARY.json, tracks usage frequencies, and enforces approved terms._

- ✅ **[T-022] Add Russian README translation**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, localization
  - _Description:_ Add a Russian localization of the README plus supporting glossary entries.
  - _Commit:_ `934d327` — Mark T-022 done after translation review
  - 💬 **Comments:**
    - **reviewer:** _Added README.ru.md plus GLOSSARY.json context so translation terminology stays consistent._

- ✅ **[T-023] Add Spanish README translation**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, localization
  - _Description:_ Deliver another Spanish README update incorporating the refined glossary process.
  - _Commit:_ `1f58561` — T-023: mark Spanish README translation done
  - 💬 **Comments:**
    - **reviewer:** _Created README.es.md and updated GLOSSARY.json with Spanish equivalents for existing terms._

- ✅ **[T-024] Revise glossary schema for translations**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, localization, glossary
  - _Description:_ Restructure the glossary so English remains canonical while localized entries store metadata per language.
  - _Commit:_ `eb5a185` — T-024: finalize glossary schema work
  - 💬 **Comments:**
    - **reviewer:** _Updated the TRANSLATOR workflow and converted GLOSSARY.json so languages own their preferred terms and descriptions._

- ✅ **[T-025] Clarify emoji commit workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, git
  - _Description:_ Clarify how commits should start with emojis and summarize completed plan items.
  - _Commit:_ `8b9cb04` — ✅ Mark T-025 done
  - 💬 **Comments:**
    - **reviewer:** _Updated AGENTS.md and README.md so commit messages start with meaningful emojis referencing the finished plan item._

- ✅ **[T-026] Enforce atomic task planning**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, planning
  - _Description:_ Ensure the PLANNER splits every request into single-owner tasks with unique commits.
  - _Commit:_ `851c576` — 🧩 T-026 enforce atomic planning
  - 💬 **Comments:**
    - **reviewer:** _Updated .AGENTS/PLANNER.json, AGENTS.md, and README.md so the PLANNER keeps tasks atomic._

- ✅ **[T-027] Add UPDATER optimization agent**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, optimization
  - _Description:_ Introduce an agent dedicated to auditing the repository and proposing optimizations to existing agents when explicitly requested.
  - _Commit:_ `1f484b2` — ✅ Review UPDATER agent deliverable (T-027)
  - 💬 **Comments:**
    - **reviewer:** _Verified .AGENTS/UPDATER.json and AGENTS.md to ensure the new agent only runs on explicit optimization requests and outputs a repo-wide optimization plan._

- ✅ **[T-028] Add virtualenv installation reminder**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** docs • **Tags:** docs, workflow
  - _Description:_ Add a global reminder that any external libraries required by scripts must be installed only inside virtual environments.
  - _Commit:_ `cc7a020` — ✅ mark T-028 done
  - 💬 **Comments:**
    - **docs:** _Added AGENTS.md guidance reminding contributors to install external dependencies only within virtual environments before running scripts._

- ✅ **[T-029] Audit agents for optimization opportunities**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** UPDATER • **Tags:** agents, optimization
  - _Description:_ Review every agent prompt and workflow the user asked about to find practical optimizations and recommend next steps.
  - _Commit:_ `32b4219` — 🧭 T-029 finish agent audit
  - 💬 **Comments:**
    - **UPDATER:** _Reported the missing glossary and CODER permission gaps plus suggested focused follow-ups._

- ✅ **[T-030] Clarify CODER agent permissions**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** CODER • **Tags:** agents, permissions
  - _Description:_ Align the CODER role with actual responsibilities by expanding permissions and workflow details per the recent request.
  - _Commit:_ `c7f224c` — 🧩 T-030 revise coder agent
  - 💬 **Comments:**
    - **CODER:** _Expanded permissions, workflow detail, and verification guidance to match the current responsibilities._

- ✅ **[T-031] Sync README with current agent lineup**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** docs • **Tags:** docs, readme
  - _Description:_ Refresh README.md so it describes the existing agents (including UPDATER), workflow rules, and repository layout that reflect the latest codebase.
  - _Commit:_ `08a0c4b` — ✅ T-031 finish README sync task
  - 💬 **Comments:**
    - **docs:** _README now mentions the UPDATER optimization agent and lifecycle so the doc mirrors the current codebase._

- ✅ **[T-032] Stylize README with icons and ASCII art**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** docs • **Tags:** docs, readme
  - _Description:_ Enhance README.md by introducing inline icons, refined formatting, and an ASCII-art title while keeping the workflow explanation intact.
  - _Commit:_ `f6eecde` — 📝 T-032 stylize README
  - 💬 **Comments:**
    - **docs:** _README now shows ASCII art, icons, and refreshed formatting so it feels more polished._
