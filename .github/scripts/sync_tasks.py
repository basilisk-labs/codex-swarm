#!/usr/bin/env python3
"""
Sync tasks.json with GitHub Issues.

Source of truth: tasks.json
Each task -> issue with label `task-id:<ID>`.

Required env:
  GITHUB_TOKEN   - classic token or fine-grained PAT with repo + project access
  GITHUB_OWNER   - e.g. "basilisk-labs"
  GITHUB_REPO    - e.g. "codex-swarm"
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

ROOT = Path(__file__).resolve().parents[2]  # repo root
TASKS_PATH = ROOT / "tasks.json"

GITHUB_API = "https://api.github.com"
OWNER = os.environ["GITHUB_OWNER"]
REPO = os.environ["GITHUB_REPO"]
TOKEN = os.environ["GITHUB_TOKEN"]

SESSION = requests.Session()
SESSION.headers.update(
    {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
)


def load_tasks() -> List[Dict[str, Any]]:
    data = json.loads(TASKS_PATH.read_text())
    return data["tasks"]


def build_labels(task: Dict[str, Any]) -> List[str]:
    labels: List[str] = []
    labels.append(f"task-id:{task['id']}")

    # status / priority / owner
    labels.append(f"status:{task['status']}")
    labels.append(f"priority:{task.get('priority', 'med')}")
    labels.append(f"owner:{task.get('owner', 'unknown')}")

    # arbitrary tags
    labels.extend(task.get("tags", []))
    return labels


def build_title(task: Dict[str, Any]) -> str:
    return f"[{task['id']}] {task['title']}"


def build_body(task: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"Internal ID: `{task['id']}`\n")

    lines.append("**Description**")
    desc = task.get("description") or "_No description provided._"
    lines.append(desc)

    lines.append("\n**Meta**")
    lines.append(f"- Status: `{task['status']}`")
    lines.append(f"- Priority: `{task.get('priority', 'med')}`")
    lines.append(f"- Owner: `{task.get('owner', 'unknown')}`")
    tags = ", ".join(task.get("tags", [])) or "none"
    lines.append(f"- Tags: `{tags}`")

    commit = task.get("commit")
    if commit:
        h = commit["hash"]
        msg = commit["message"]
        url = f"https://github.com/{OWNER}/{REPO}/commit/{h}"
        lines.append(f"- Commit: [`{h[:7]}`]({url}) — {msg}")

    lines.append(
        "\n_This issue is synced from `tasks.json`. "
        "Change status and details in that file, not here._"
    )
    return "\n".join(lines)


def find_issue_by_task_id(task_id: str) -> Optional[Dict[str, Any]]:
    """Search issue by label task-id:<id>. Returns first match or None."""
    label = f"task-id:{task_id}"
    url = f"{GITHUB_API}/repos/{OWNER}/{REPO}/issues"
    params = {"labels": label, "state": "all", "per_page": 50}
    r = SESSION.get(url, params=params)
    r.raise_for_status()
    issues = r.json()
    return issues[0] if issues else None


def create_issue(task: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{GITHUB_API}/repos/{OWNER}/{REPO}/issues"
    data = {
        "title": build_title(task),
        "body": build_body(task),
        "labels": build_labels(task),
    }
    r = SESSION.post(url, json=data)
    r.raise_for_status()
    return r.json()


def update_issue(issue: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, Any]:
    number = issue["number"]
    url = f"{GITHUB_API}/repos/{OWNER}/{REPO}/issues/{number}"

    desired_state = "closed" if task["status"] == "DONE" else "open"

    data = {
        "title": build_title(task),
        "body": build_body(task),
        "labels": build_labels(task),
        "state": desired_state,
    }
    r = SESSION.patch(url, json=data)
    r.raise_for_status()
    return r.json()


def sync() -> None:
    tasks = load_tasks()
    for task in tasks:
        task_id = task["id"]
        issue = find_issue_by_task_id(task_id)
        if issue is None:
            print(f"[+] create issue for {task_id}")
            create_issue(task)
        else:
            print(f"[*] update issue #{issue['number']} for {task_id}")
            update_issue(issue, task)


if __name__ == "__main__":
    sync()
