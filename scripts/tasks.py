#!/usr/bin/env python3
"""Render tasks.md from the canonical tasks.json file."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from typing import Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
TASKS_PATH = ROOT / "tasks.json"
OUTPUT_PATH = ROOT / "tasks.md"

STATUS_SECTIONS = [
    ("TODO", "📋 Backlog", "_No open tasks._"),
    ("DOING", "🚧 In Progress", "_No active tasks._"),
    ("BLOCKED", "⛔ Blocked", "_No blocked tasks._"),
    ("DONE", "✅ Done", "_No completed tasks yet._"),
]

STATUS_SYMBOLS = {
    "TODO": "📝",
    "DOING": "⚙️",
    "BLOCKED": "🛑",
    "DONE": "✅",
}

SUMMARY_ICONS = {
    "TOTAL": "🧮",
    "TODO": "📋",
    "DOING": "🚧",
    "BLOCKED": "⛔",
    "DONE": "✅",
}

STATUS_LABELS = {
    "TODO": "Backlog",
    "DOING": "In Progress",
    "BLOCKED": "Blocked",
    "DONE": "Done",
}

AGENT_ICONS = {
    "CODEX": "🤖",
    "DOCS": "📚",
    "CODER": "🛠️",
    "REVIEWER": "👀",
    "UPDATER": "🔍",
    "PLANNER": "🗺️",
    "CREATOR": "🏗️",
}
DEFAULT_AGENT_ICON = "🧠"


def get_current_branch() -> Optional[str]:
    """Return the current git branch name, or None if it cannot be determined."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    branch = (result.stdout or "").strip()
    return branch or None


def normalize_remote_url(url: str) -> Optional[str]:
    raw = (url or "").strip()
    if not raw:
        return None
    if raw.startswith("git@"):
        raw = raw.replace(":", "/", 1)
        raw = raw.replace("git@", "https://", 1)
    elif raw.startswith("ssh://"):
        raw = raw[len("ssh://") :]
        if raw.startswith("git@"):
            raw = raw.replace("git@", "https://", 1)
        else:
            raw = "https://" + raw
    elif not (raw.startswith("http://") or raw.startswith("https://")):
        return None
    if raw.endswith(".git"):
        raw = raw[:-4]
    return raw


def get_repo_commit_base() -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return normalize_remote_url(result.stdout)


REPO_COMMIT_BASE = get_repo_commit_base()


def codeify(value: str) -> str:
    return f"`{value}`"


def format_owner_value(owner: Optional[str]) -> str:
    owner_text = (owner or "").strip()
    if not owner_text:
        return codeify("-")
    owner_upper = owner_text.upper()
    icon = AGENT_ICONS.get(owner_upper, DEFAULT_AGENT_ICON)
    return codeify(f"{icon} {owner_upper}")


def format_tags_value(tags: List[str]) -> str:
    if not tags:
        return codeify("-")
    return ", ".join(codeify(tag) for tag in tags)


def load_tasks_data() -> Dict[str, List[Dict]]:
    with TASKS_PATH.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError("tasks.json must contain a top-level 'tasks' list")
    return {"tasks": tasks}


def sorted_tasks(tasks: List[Dict]) -> List[Dict]:
    return sorted(tasks, key=lambda task: task.get("id", ""))


COMMIT_DELIMITER = "\x1f"


def find_commit_for_task(task_id: str) -> Optional[Dict[str, str]]:
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--grep",
                task_id,
                "-n",
                "1",
                f"--pretty=format:%H{COMMIT_DELIMITER}%s",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return None
    line = result.stdout.strip().splitlines()
    if not line:
        return None
    parts = line[0].split(COMMIT_DELIMITER, 1)
    if not parts or not parts[0]:
        return None
    commit_hash = parts[0]
    commit_message = parts[1] if len(parts) > 1 else ""
    return {"hash": commit_hash, "message": commit_message}


def ensure_commit_metadata(tasks: List[Dict]) -> bool:
    updated = False
    for task in tasks:
        if task.get("status") != "DONE":
            continue
        if task.get("commit"):
            continue
        task_id = task.get("id")
        if not task_id:
            continue
        commit_info = find_commit_for_task(task_id)
        if not commit_info:
            continue
        task["commit"] = commit_info
        updated = True
    return updated


def persist_tasks_data(data: Dict[str, List[Dict]]) -> None:
    TASKS_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def format_metadata(task: Dict) -> str:
    priority_value = codeify(str(task.get("priority", "-")))
    owner_value = format_owner_value(task.get("owner"))
    tags_value = format_tags_value(task.get("tags") or [])
    return f"**Priority:** {priority_value} • **Owner:** {owner_value} • **Tags:** {tags_value}"


def format_description(task: Dict) -> str:
    description = (task.get("description") or "").strip()
    return description if description else "No description provided."


def build_commit_link(commit_hash: str) -> Optional[str]:
    if not REPO_COMMIT_BASE:
        return None
    return f"{REPO_COMMIT_BASE}/commit/{commit_hash}"


def format_commit_line(task: Dict) -> Optional[str]:
    commit = task.get("commit")
    if not commit:
        return None
    commit_hash = (commit.get("hash") or "").strip()
    if not commit_hash:
        return None
    short_hash = commit_hash[:7]
    commit_message = (commit.get("message") or "").strip()
    link = build_commit_link(commit_hash)
    hash_display = (
        f"[`{short_hash}`]({link})" if link else f"`{short_hash}`"
    )
    if commit_message:
        return f"  - **_Commit:_** {hash_display} — {commit_message}"
    return f"  - **_Commit:_** {hash_display}"


def format_comments(task: Dict) -> List[str]:
    comments = task.get("comments") or []
    formatted: List[str] = []
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        author = comment.get("author", "unknown") or "unknown"
        body = (comment.get("body") or "").strip()
        body = body if body else "(no additional details)"
        formatted.append(f"    - **{author}:** _{body}_")
    if not formatted:
        formatted.append("    - _No comments yet._")
    return formatted


def build_section(tasks: List[Dict], status: str, heading: str, empty_text: str) -> List[str]:
    block: List[str] = [f"## **{heading}**"]
    section_tasks = [task for task in tasks if task.get("status") == status]
    if not section_tasks:
        block.append(empty_text)
        return block
    for task in section_tasks:
        symbol = STATUS_SYMBOLS.get(status, "[?]")
        task_id = task.get("id", "<no-id>")
        title = task.get("title", "(untitled task)")
        block.append(f"- {symbol} **[{task_id}] {title}**")
        block.append(f"  - **_Status:_** *{STATUS_LABELS.get(status, 'Unknown')}*")
        block.append(f"  - {format_metadata(task)}")
        block.append(f"  - **Description:** {format_description(task)}")
        commit_line = format_commit_line(task)
        if commit_line:
            block.append(commit_line)
        block.append("  - 💬 **Comments:**")
        block.extend(format_comments(task))
        block.append("")
    if block[-1] == "":
        block.pop()
    return block


def main() -> None:
    branch = get_current_branch()
    if branch is None:
        print("Could not determine git branch; skipping tasks.md generation.")
        return
    if branch != "main":
        print(f"Skipping tasks.md generation on non-main branch: {branch}")
        return

    data = load_tasks_data()
    tasks = data["tasks"]
    if ensure_commit_metadata(tasks):
        persist_tasks_data(data)
        print("Updated tasks.json with commit metadata.")
    tasks = sorted_tasks(tasks)
    counts: Dict[str, int] = {status: 0 for status, *_ in STATUS_SECTIONS}
    for task in tasks:
        status = task.get("status")
        if status in counts:
            counts[status] += 1
    total_tasks = len(tasks)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: List[str] = ["# ✨ Project Tasks Board", "", f"_Last updated: {now}_", "", "## **⭐ Summary**", ""]
    lines.append("| Icon | Metric | Count |")
    lines.append("| --- | --- | --- |")
    lines.append(f"| {SUMMARY_ICONS['TOTAL']} | **Total** | {total_tasks} |")
    for status, heading, _ in STATUS_SECTIONS:
        label = STATUS_LABELS.get(status, heading)
        icon = SUMMARY_ICONS.get(status, "•")
        lines.append(f"| {icon} | **{label}** | {counts.get(status, 0)} |")
    lines.append("")
    lines.append("🌈 **Palette note:** Keep `python scripts/tasks.py` handy so the table stays in sync after every update.")
    lines.append("🎉 **Vibe check:** Emoji commits + clear summaries = joyful collaborators.")
    lines.append("")

    for status, heading, empty_text in STATUS_SECTIONS:
        lines.extend(build_section(tasks, status, heading, empty_text))
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {total_tasks} tasks.")


if __name__ == "__main__":
    main()
