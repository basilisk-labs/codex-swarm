# ✨ Project Tasks Board

_Last updated: 2025-11-21 15:52:04 UTC_

## ⭐ Summary
- 🧮 **Total:** 29
- 📋 **Backlog:** 0
- 🚧 **In Progress:** 1
- ⛔ **Blocked:** 0
- ✅ **Done:** 28

## 📋 Backlog
_No open tasks._

## 🚧 In Progress
- ⚙️ **[T-029] Audit agents for optimization opportunities**
  - _Status:_ *In Progress*
  - **Priority:** high • **Owner:** UPDATER • **Tags:** agents, optimization
  - _Description:_ Review every agent prompt and workflow the user asked about to find practical optimizations and recommend next steps.
  - 💬 **Comments:**
    - _No comments yet._

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
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-005] Document commit workflow in README**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, workflow
  - _Description:_ Expand the README with details on emoji commits and atomic task tracking.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-006] Add Agent Creator workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, automation
  - _Description:_ Describe how new specialist agents are proposed, reviewed, and added to the registry.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-007] Improve commit message guidance**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, git
  - _Description:_ Tighten the instructions around writing meaningful, emoji-prefixed commit messages.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-008] Document repository structure in README**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, readme
  - _Description:_ Add a quick-start tour of key files and directories so contributors know where to work.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-009] Define status transition protocol**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, tasks
  - _Description:_ Clarify which agent owns each state change and how statuses move between TODO/DOING/DONE/BLOCKED.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-010] Automate agent registry updates**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** agents, automation
  - _Description:_ Explain how the orchestrator scans .AGENTS/*.json dynamically instead of relying on a manual list.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-011] Evaluate workflow and suggest improvements**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** workflow, analysis
  - _Description:_ Review the end-to-end authoring flow and capture improvement ideas inside the docs.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-012] Generalize AGENTS.md to remove agent-specific guidance**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Keep AGENTS.md focused on cross-agent protocol instead of baking in individual instructions.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-013] Align agent prompts with GPT-5.1 guide**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** prompting, agents
  - _Description:_ Update every agent spec so prompts match the GPT-5.1 best practices.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-014] Document Cursor + Codex local workflow in AGENTS.md**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Add environment assumptions for local-only workflows without remote runtimes.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-015] Align agent prompts with Cursor + Codex constraints**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** prompting, agents
  - _Description:_ Ensure prompts mention the IDE limitations so agents avoid referencing unavailable tools.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-016] Remove tool references from AGENTS.md for Codex-only workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Strip references to unsupported helper tools to keep instructions aligned with the local stack.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-017] Update agent prompts for tool-less Codex context**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** prompting, agents
  - _Description:_ Reword prompts so agents do not assume access to external search or commands.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-018] Streamline AGENTS.md English guidelines**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, agents
  - _Description:_ Trim redundant English-language instructions and keep the doc crisp.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-019] Add glossary-aware translation agent**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, localization
  - _Description:_ Introduce a translator agent that respects glossary entries when localizing README content.
  - 💬 **Comments:**
    - _No comments yet._

- ✅ **[T-020] Add Spanish README translation**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, localization
  - _Description:_ Provide a Spanish version of the README while keeping glossary terms consistent.
  - 💬 **Comments:**
    - **reviewer:** _Added README.es.md and ensured glossary coverage for Spanish terminology._

- ✅ **[T-021] Enhance translator glossary workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, localization
  - _Description:_ Teach the translator agent how to maintain glossary metadata and usage counts automatically.
  - 💬 **Comments:**
    - **reviewer:** _Updated the TRANSLATOR agent so every run maintains GLOSSARY.json, tracks usage frequencies, and enforces approved terms._

- ✅ **[T-022] Add Russian README translation**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, localization
  - _Description:_ Add a Russian localization of the README plus supporting glossary entries.
  - 💬 **Comments:**
    - **reviewer:** _Added README.ru.md plus GLOSSARY.json context so translation terminology stays consistent._

- ✅ **[T-023] Add Spanish README translation**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** codex • **Tags:** docs, localization
  - _Description:_ Deliver another Spanish README update incorporating the refined glossary process.
  - 💬 **Comments:**
    - **reviewer:** _Created README.es.md and updated GLOSSARY.json with Spanish equivalents for existing terms._

- ✅ **[T-024] Revise glossary schema for translations**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** docs, localization, glossary
  - _Description:_ Restructure the glossary so English remains canonical while localized entries store metadata per language.
  - 💬 **Comments:**
    - **reviewer:** _Updated the TRANSLATOR workflow and converted GLOSSARY.json so languages own their preferred terms and descriptions._

- ✅ **[T-025] Clarify emoji commit workflow**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, git
  - _Description:_ Clarify how commits should start with emojis and summarize completed plan items.
  - 💬 **Comments:**
    - **reviewer:** _Updated AGENTS.md and README.md so commit messages start with meaningful emojis referencing the finished plan item._

- ✅ **[T-026] Enforce atomic task planning**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** workflow, planning
  - _Description:_ Ensure the PLANNER splits every request into single-owner tasks with unique commits.
  - 💬 **Comments:**
    - **reviewer:** _Updated .AGENTS/PLANNER.json, AGENTS.md, and README.md so the PLANNER keeps tasks atomic._

- ✅ **[T-027] Add UPDATER optimization agent**
  - _Status:_ *Done*
  - **Priority:** high • **Owner:** codex • **Tags:** agents, optimization
  - _Description:_ Introduce an agent dedicated to auditing the repository and proposing optimizations to existing agents when explicitly requested.
  - 💬 **Comments:**
    - **reviewer:** _Verified .AGENTS/UPDATER.json and AGENTS.md to ensure the new agent only runs on explicit optimization requests and outputs a repo-wide optimization plan._

- ✅ **[T-028] Add virtualenv installation reminder**
  - _Status:_ *Done*
  - **Priority:** med • **Owner:** docs • **Tags:** docs, workflow
  - _Description:_ Add a global reminder that any external libraries required by scripts must be installed only inside virtual environments.
  - 💬 **Comments:**
    - **docs:** _Added AGENTS.md guidance reminding contributors to install external dependencies only within virtual environments before running scripts._
