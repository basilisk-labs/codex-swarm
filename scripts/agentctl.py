#!/usr/bin/env python3
"""Codex Swarm Agent Helper.

This script automates repetitive, error-prone steps that show up across agent
workflows (readiness checks, safe tasks.json updates, and git hygiene).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SWARM_DIR = ROOT / ".codex-swarm"
SWARM_CONFIG_PATH = SWARM_DIR / "swarm-config.json"

ALLOWED_STATUSES: Set[str] = {"TODO", "DOING", "BLOCKED", "DONE"}
TASKS_SCHEMA_VERSION = 1
TASKS_META_KEY = "meta"
TASKS_META_MANAGED_BY = "agentctl"

GENERIC_COMMIT_TOKENS: Set[str] = {
    "start",
    "status",
    "mark",
    "done",
    "wip",
    "update",
    "tasks",
    "task",
}


def run(cmd: List[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=check,
    )


def die(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def commit_message_has_meaningful_summary(task_id: str, message: str) -> bool:
    task_token = task_id.strip().lower()
    if not task_token:
        return True
    tokens = re.findall(r"[0-9A-Za-zА-Яа-яЁё]+(?:-[0-9A-Za-zА-Яа-яЁё]+)*", message.lower())
    meaningful = [t for t in tokens if t != task_token and t not in GENERIC_COMMIT_TOKENS]
    return bool(meaningful)


def require_structured_comment(body: str, *, prefix: str, min_chars: int) -> None:
    normalized = (body or "").strip()
    if not normalized.lower().startswith(prefix.lower()):
        die(f"Comment body must start with {prefix!r}", code=2)
    if len(normalized) < min_chars:
        die(f"Comment body must be at least {min_chars} characters", code=2)


def load_json(path: Path) -> Dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"Missing file: {path}")
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON in {path}: {exc}")


def _resolve_repo_relative_path(value: str, *, label: str) -> Path:
    raw = str(value or "").strip()
    if not raw:
        die(f"Missing config path for {label!r} in {SWARM_CONFIG_PATH}")
    path = Path(raw)
    if path.is_absolute():
        die(f"Config path for {label!r} must be repo-relative (got absolute path: {raw})")
    resolved = (ROOT / path).resolve()
    root_resolved = ROOT.resolve()
    if root_resolved not in resolved.parents and resolved != root_resolved:
        die(f"Config path for {label!r} must stay under repo root (got: {raw})")
    return resolved


def load_swarm_config() -> Dict:
    if not SWARM_CONFIG_PATH.exists():
        die(f"Missing swarm config: {SWARM_CONFIG_PATH}", code=2)
    data = load_json(SWARM_CONFIG_PATH)
    if not isinstance(data, dict):
        die(f"{SWARM_CONFIG_PATH} must contain a JSON object", code=2)
    schema_version = data.get("schema_version")
    if schema_version != 1:
        die(f"Unsupported swarm config schema_version: {schema_version!r} (expected 1)", code=2)
    paths = data.get("paths")
    if not isinstance(paths, dict):
        die(f"{SWARM_CONFIG_PATH} must contain a top-level 'paths' object", code=2)
    return data


_SWARM_CONFIG = load_swarm_config()
_PATHS = _SWARM_CONFIG.get("paths") or {}
TASKS_PATH = _resolve_repo_relative_path(_PATHS.get("tasks_path"), label="tasks_path")
AGENTS_DIR = _resolve_repo_relative_path(_PATHS.get("agents_dir"), label="agents_dir")
AGENTCTL_DOCS_PATH = _resolve_repo_relative_path(_PATHS.get("agentctl_docs_path"), label="agentctl_docs_path")
WORKFLOW_DIR = _resolve_repo_relative_path(_PATHS.get("workflow_dir"), label="workflow_dir")


def write_json(path: Path, data: Dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical_tasks_payload(tasks: List[Dict]) -> str:
    return json.dumps({"tasks": tasks}, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def compute_tasks_checksum(tasks: List[Dict]) -> str:
    payload = canonical_tasks_payload(tasks).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def update_tasks_meta(data: Dict) -> None:
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        return
    meta = data.get(TASKS_META_KEY)
    if not isinstance(meta, dict):
        meta = {}
    meta["schema_version"] = TASKS_SCHEMA_VERSION
    meta["managed_by"] = TASKS_META_MANAGED_BY
    meta["checksum_algo"] = "sha256"
    meta["checksum"] = compute_tasks_checksum(tasks)
    data[TASKS_META_KEY] = meta


def write_tasks_json(data: Dict) -> None:
    update_tasks_meta(data)
    write_json(TASKS_PATH, data)


def load_tasks() -> List[Dict]:
    data = load_json(TASKS_PATH)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            die(f"tasks.json tasks[{index}] must be an object")
    return tasks


def format_task_line(task: Dict) -> str:
    task_id = str(task.get("id") or "").strip()
    title = str(task.get("title") or "").strip() or "(untitled task)"
    status = str(task.get("status") or "TODO").strip().upper()
    return f"{task_id} [{status}] {title}"


def cmd_task_list(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    tasks_by_id, warnings = index_tasks_by_id(tasks)
    if warnings and not args.quiet:
        for warning in warnings:
            print(f"⚠️ {warning}")
    tasks_sorted = sorted(tasks_by_id.values(), key=lambda t: str(t.get("id") or ""))
    if args.status:
        want = {s.strip().upper() for s in args.status}
        tasks_sorted = [t for t in tasks_sorted if str(t.get("status") or "TODO").strip().upper() in want]
    if args.owner:
        want_owner = {o.strip().upper() for o in args.owner}
        tasks_sorted = [t for t in tasks_sorted if str(t.get("owner") or "").strip().upper() in want_owner]
    if args.tag:
        want_tag = {t.strip() for t in args.tag}
        filtered: List[Dict] = []
        for task in tasks_sorted:
            tags = task.get("tags") or []
            if any(tag in want_tag for tag in tags if isinstance(tag, str)):
                filtered.append(task)
        tasks_sorted = filtered
    for task in tasks_sorted:
        print(format_task_line(task))


def cmd_task_next(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    tasks_by_id, warnings = index_tasks_by_id(tasks)
    dep_state, dep_warnings = compute_dependency_state(tasks_by_id)
    warnings = warnings + dep_warnings
    if warnings and not args.quiet:
        for warning in warnings:
            print(f"⚠️ {warning}")

    tasks_sorted = sorted(tasks_by_id.values(), key=lambda t: str(t.get("id") or ""))
    statuses = {s.strip().upper() for s in (args.status or ["TODO"])}
    tasks_sorted = [t for t in tasks_sorted if str(t.get("status") or "TODO").strip().upper() in statuses]

    if args.owner:
        want_owner = {o.strip().upper() for o in args.owner}
        tasks_sorted = [t for t in tasks_sorted if str(t.get("owner") or "").strip().upper() in want_owner]
    if args.tag:
        want_tag = {t.strip() for t in args.tag}
        filtered: List[Dict] = []
        for task in tasks_sorted:
            tags = task.get("tags") or []
            if any(tag in want_tag for tag in tags if isinstance(tag, str)):
                filtered.append(task)
        tasks_sorted = filtered

    ready_tasks: List[Dict] = []
    for task in tasks_sorted:
        task_id = str(task.get("id") or "").strip()
        info = dep_state.get(task_id) or {}
        missing = info.get("missing") or []
        incomplete = info.get("incomplete") or []
        if missing or incomplete:
            continue
        ready_tasks.append(task)

    if args.limit is not None and args.limit >= 0:
        ready_tasks = ready_tasks[: args.limit]
    for task in ready_tasks:
        print(format_task_line(task))


def _task_text_blob(task: Dict) -> str:
    parts: List[str] = []
    for key in ("id", "title", "description", "status", "priority", "owner"):
        value = task.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    tags = task.get("tags")
    if isinstance(tags, list):
        parts.extend(t for t in tags if isinstance(t, str) and t.strip())
    comments = task.get("comments")
    if isinstance(comments, list):
        for comment in comments:
            if not isinstance(comment, dict):
                continue
            author = comment.get("author")
            body = comment.get("body")
            if isinstance(author, str) and author.strip():
                parts.append(author.strip())
            if isinstance(body, str) and body.strip():
                parts.append(body.strip())
    commit = task.get("commit")
    if isinstance(commit, dict):
        for key in ("hash", "message"):
            value = commit.get(key)
            if isinstance(value, str) and value.strip():
                parts.append(value.strip())
    return "\n".join(parts)


def cmd_task_search(args: argparse.Namespace) -> None:
    query = args.query.strip()
    if not query:
        die("Query must be non-empty", code=2)

    tasks = load_tasks()
    tasks_by_id, warnings = index_tasks_by_id(tasks)
    if warnings and not args.quiet:
        for warning in warnings:
            print(f"⚠️ {warning}")

    tasks_sorted = sorted(tasks_by_id.values(), key=lambda t: str(t.get("id") or ""))
    if args.status:
        want = {s.strip().upper() for s in args.status}
        tasks_sorted = [t for t in tasks_sorted if str(t.get("status") or "TODO").strip().upper() in want]
    if args.owner:
        want_owner = {o.strip().upper() for o in args.owner}
        tasks_sorted = [t for t in tasks_sorted if str(t.get("owner") or "").strip().upper() in want_owner]
    if args.tag:
        want_tag = {t.strip() for t in args.tag}
        filtered: List[Dict] = []
        for task in tasks_sorted:
            tags = task.get("tags") or []
            if any(tag in want_tag for tag in tags if isinstance(tag, str)):
                filtered.append(task)
        tasks_sorted = filtered

    if args.regex:
        try:
            pattern = re.compile(query, flags=re.IGNORECASE)
        except re.error as exc:
            die(f"Invalid regex: {exc}", code=2)
        matches = [t for t in tasks_sorted if pattern.search(_task_text_blob(t) or "")]
    else:
        q = query.lower()
        matches = [t for t in tasks_sorted if q in (_task_text_blob(t) or "").lower()]

    if args.limit is not None and args.limit >= 0:
        matches = matches[: args.limit]
    for task in matches:
        print(format_task_line(task))


def cmd_task_scaffold(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)

    title = args.title
    if not title and not args.force:
        data = load_json(TASKS_PATH)
        task = _ensure_task_object(data, task_id)
        title = str(task.get("title") or "").strip()

    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
    target = WORKFLOW_DIR / f"{task_id}.md"
    if target.exists() and not args.overwrite:
        die(f"File already exists: {target}", code=2)

    heading = f"# {task_id}: {title.strip()}" if title and title.strip() else f"# {task_id}"
    content = "\n".join(
        [
            heading,
            "",
            "## Goal",
            "",
            "- ...",
            "",
            "## Scope",
            "",
            "- ...",
            "",
            "## Verification",
            "",
            "- ...",
            "",
        ]
    )
    target.write_text(content, encoding="utf-8")
    if not args.quiet:
        print(f"✅ wrote {target.relative_to(ROOT)}")


def cmd_task_show(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    tasks_by_id, warnings = index_tasks_by_id(tasks)
    if warnings and not args.quiet:
        for warning in warnings:
            print(f"⚠️ {warning}")
    task = tasks_by_id.get(args.task_id)
    if not task:
        die(f"Unknown task id: {args.task_id}")

    task_id = str(task.get("id") or "").strip()
    print(f"ID: {task_id}")
    print(f"Title: {str(task.get('title') or '').strip()}")
    print(f"Status: {str(task.get('status') or 'TODO').strip().upper()}")
    print(f"Priority: {str(task.get('priority') or '-').strip()}")
    owner = str(task.get("owner") or "-").strip()
    print(f"Owner: {owner if owner else '-'}")
    depends_on, _ = normalize_depends_on(task.get("depends_on"))
    print(f"Depends on: {', '.join(depends_on) if depends_on else '-'}")
    tags = task.get("tags") or []
    tags_str = ", ".join(t for t in tags if isinstance(t, str))
    print(f"Tags: {tags_str if tags_str else '-'}")
    description = str(task.get("description") or "").strip()
    if description:
        print("")
        print("Description:")
        print(description)
    commit = task.get("commit") or {}
    if isinstance(commit, dict) and commit.get("hash"):
        print("")
        print("Commit:")
        print(f"{commit.get('hash')} {commit.get('message') or ''}".rstrip())
    comments = task.get("comments") or []
    if isinstance(comments, list) and comments:
        print("")
        print("Comments:")
        for comment in comments[-args.last_comments :]:
            if not isinstance(comment, dict):
                continue
            author = str(comment.get("author") or "unknown")
            body = str(comment.get("body") or "").strip()
            print(f"- {author}: {body}")


def index_tasks_by_id(tasks: List[Dict]) -> Tuple[Dict[str, Dict], List[str]]:
    warnings: List[str] = []
    tasks_by_id: Dict[str, Dict] = {}
    for index, task in enumerate(tasks):
        task_id = (task.get("id") or "").strip()
        if not task_id:
            warnings.append(f"tasks[{index}] is missing a non-empty id")
            continue
        if task_id in tasks_by_id:
            warnings.append(f"Duplicate task id found: {task_id} (keeping first, ignoring later entries)")
            continue
        tasks_by_id[task_id] = task
    return tasks_by_id, warnings


def normalize_depends_on(value: object) -> Tuple[List[str], List[str]]:
    if value is None:
        return [], []
    if not isinstance(value, list):
        return [], ["depends_on must be a list of task IDs"]
    errors: List[str] = []
    normalized: List[str] = []
    seen: Set[str] = set()
    for raw in value:
        if not isinstance(raw, str):
            errors.append("depends_on entries must be strings")
            continue
        task_id = raw.strip()
        if not task_id or task_id in seen:
            continue
        seen.add(task_id)
        normalized.append(task_id)
    return normalized, errors


def detect_cycles(edges: Dict[str, List[str]]) -> List[List[str]]:
    cycles: List[List[str]] = []
    visiting: Set[str] = set()
    visited: Set[str] = set()
    stack: List[str] = []

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            if node in stack:
                start = stack.index(node)
                cycles.append(stack[start:] + [node])
            return
        visiting.add(node)
        stack.append(node)
        for dep in edges.get(node, []):
            if dep in edges:
                visit(dep)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in edges:
        visit(node)
    return cycles


def compute_dependency_state(tasks_by_id: Dict[str, Dict]) -> Tuple[Dict[str, Dict[str, List[str]]], List[str]]:
    warnings: List[str] = []
    state: Dict[str, Dict[str, List[str]]] = {}
    edges: Dict[str, List[str]] = {}

    for task_id, task in tasks_by_id.items():
        depends_on, dep_errors = normalize_depends_on(task.get("depends_on"))
        if dep_errors:
            warnings.append(f"{task_id}: " + "; ".join(sorted(set(dep_errors))))
        if task_id in depends_on:
            warnings.append(f"{task_id}: depends_on contains itself")
        missing: List[str] = []
        incomplete: List[str] = []
        for dep_id in depends_on:
            dep_task = tasks_by_id.get(dep_id)
            if not dep_task:
                missing.append(dep_id)
                continue
            if dep_task.get("status") != "DONE":
                incomplete.append(dep_id)
        state[task_id] = {
            "depends_on": depends_on,
            "missing": sorted(set(missing)),
            "incomplete": sorted(set(incomplete)),
        }
        edges[task_id] = depends_on

    cycles = detect_cycles(edges)
    if cycles:
        for cycle in cycles:
            warnings.append("Dependency cycle detected: " + " -> ".join(cycle))

    return state, warnings


def readiness(task_id: str) -> Tuple[bool, List[str]]:
    tasks = load_tasks()
    tasks_by_id, index_warnings = index_tasks_by_id(tasks)
    dep_state, dep_warnings = compute_dependency_state(tasks_by_id)
    warnings = index_warnings + dep_warnings

    task = tasks_by_id.get(task_id)
    if not task:
        return False, warnings + [f"Unknown task id: {task_id}"]

    info = dep_state.get(task_id) or {}
    missing = info.get("missing") or []
    incomplete = info.get("incomplete") or []

    if missing:
        warnings.append(f"{task_id}: missing deps: {', '.join(missing)}")
    if incomplete:
        warnings.append(f"{task_id}: incomplete deps: {', '.join(incomplete)}")

    return (not missing and not incomplete), warnings


def get_commit_info(rev: str) -> Dict[str, str]:
    try:
        result = run(["git", "show", "-s", "--pretty=format:%H\x1f%s", rev], check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or f"Failed to resolve git revision: {rev}")
    raw = (result.stdout or "").strip()
    if "\x1f" not in raw:
        die(f"Unexpected git output for rev {rev}")
    commit_hash, subject = raw.split("\x1f", 1)
    return {"hash": commit_hash.strip(), "message": subject.strip()}


def git_staged_files() -> List[str]:
    try:
        result = run(["git", "diff", "--name-only", "--cached"], check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to read staged files")
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def git_unstaged_files() -> List[str]:
    try:
        result = run(["git", "diff", "--name-only"], check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to read unstaged files")
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def suggest_allow_prefixes(paths: Iterable[str]) -> List[str]:
    prefixes: List[str] = []
    for raw in paths:
        path = raw.strip().lstrip("./")
        if not path:
            continue
        if "/" not in path:
            prefixes.append(path)
            continue
        prefixes.append(path.rsplit("/", 1)[0])
    return sorted(set(prefixes))


def path_is_under(path: str, prefix: str) -> bool:
    p = path.strip().lstrip("./")
    root = prefix.strip().lstrip("./").rstrip("/")
    if not root:
        return False
    return p == root or p.startswith(root + "/")


def guard_commit_check(
    *,
    task_id: str,
    message: str,
    allow: List[str],
    allow_tasks: bool,
    require_clean: bool,
    quiet: bool,
) -> None:
    if task_id not in message:
        die(f"Commit message must include {task_id}", code=2)
    if not commit_message_has_meaningful_summary(task_id, message):
        die(
            "Commit message is too generic; include a short summary (and constraints when relevant), "
            'e.g. "✨ T-123 Add X (no network)"',
            code=2,
        )

    staged = git_staged_files()
    if not staged:
        die("No staged files", code=2)

    if not allow:
        die("Provide at least one --allow <path> prefix", code=2)

    unstaged = git_unstaged_files()
    if require_clean and unstaged:
        for path in unstaged:
            print(f"❌ unstaged: {path}", file=sys.stderr)
        die("Working tree is dirty", code=2)
    if unstaged and not quiet and not require_clean:
        print(f"⚠️ working tree has {len(unstaged)} unstaged file(s); ignoring (multi-agent workspace)")

    denied = set()
    if not allow_tasks:
        denied.update({"tasks.json"})

    for path in staged:
        if path in denied:
            die(f"Staged file is forbidden by default: {path} (use --allow-tasks to override)", code=2)
        if not any(path_is_under(path, allowed) for allowed in allow):
            die(f"Staged file is outside allowlist: {path}", code=2)

    if not quiet:
        print("✅ guard passed")

def cmd_agents(_: argparse.Namespace) -> None:
    if not AGENTS_DIR.exists():
        die(f"Missing directory: {AGENTS_DIR}")
    paths = sorted(AGENTS_DIR.glob("*.json"))
    if not paths:
        die(f"No agents found under {AGENTS_DIR}")

    rows: List[Tuple[str, str, str]] = []
    seen: Dict[str, str] = {}
    duplicates: List[str] = []
    for path in paths:
        data = load_json(path)
        agent_id = str(data.get("id") or "").strip()
        role = str(data.get("role") or "").strip()
        if not agent_id:
            agent_id = "<missing-id>"
        if agent_id in seen:
            duplicates.append(agent_id)
        else:
            seen[agent_id] = path.name
        rows.append((agent_id, role or "-", path.name))

    width_id = max(len(r[0]) for r in rows + [("ID", "", "")])
    width_file = max(len(r[2]) for r in rows + [("", "", "FILE")])
    print(f"{'ID'.ljust(width_id)}  {'FILE'.ljust(width_file)}  ROLE")
    print(f"{'-'*width_id}  {'-'*width_file}  {'-'*4}")
    for agent_id, role, filename in rows:
        print(f"{agent_id.ljust(width_id)}  {filename.ljust(width_file)}  {role}")

    if duplicates:
        die(f"Duplicate agent ids: {', '.join(sorted(set(duplicates)))}", code=2)


def cmd_quickstart(_: argparse.Namespace) -> None:
    if AGENTCTL_DOCS_PATH.exists():
        print(AGENTCTL_DOCS_PATH.read_text(encoding="utf-8").rstrip())
        return
    print(
        "\n".join(
            [
                "agentctl quickstart",
                "",
                "This repo uses python scripts/agentctl.py to manage tasks.json safely (no manual edits).",
                "",
                "Common commands:",
                "  python scripts/agentctl.py task list",
                "  python scripts/agentctl.py task show T-123",
                "  python scripts/agentctl.py task lint",
                "  python scripts/agentctl.py ready T-123",
                "  python scripts/agentctl.py start T-123 --author CODER --body \"Start: ...\"",
                "  python scripts/agentctl.py verify T-123",
                "  python scripts/agentctl.py guard commit T-123 -m \"✨ T-123 ...\" --allow <path-prefix>",
                "  python scripts/agentctl.py finish T-123 --commit <git-rev> --author REVIEWER --body \"Verified: ...\"",
                "",
                f"Tip: create {AGENTCTL_DOCS_PATH.as_posix()} to override this output.",
            ]
        )
    )


def load_agents_index() -> Set[str]:
    if not AGENTS_DIR.exists():
        return set()
    ids: Set[str] = set()
    for path in sorted(AGENTS_DIR.glob("*.json")):
        data = load_json(path)
        agent_id = str(data.get("id") or "").strip().upper()
        if agent_id:
            ids.add(agent_id)
    return ids


def lint_tasks_json() -> Dict[str, List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    data = load_json(TASKS_PATH)
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        return {"errors": ["tasks.json must contain a top-level 'tasks' list"], "warnings": []}

    meta = data.get(TASKS_META_KEY)
    if not isinstance(meta, dict):
        errors.append("tasks.json is missing a top-level 'meta' object (manual edits are not allowed)")
    else:
        expected = compute_tasks_checksum(tasks)
        checksum = str(meta.get("checksum") or "")
        algo = str(meta.get("checksum_algo") or "")
        managed_by = str(meta.get("managed_by") or "")
        if algo != "sha256":
            errors.append("tasks.json meta.checksum_algo must be 'sha256'")
        if managed_by != TASKS_META_MANAGED_BY:
            errors.append("tasks.json meta.managed_by must be 'agentctl'")
        if not checksum:
            errors.append("tasks.json meta.checksum is missing/empty")
        elif checksum != expected:
            errors.append("tasks.json meta.checksum does not match tasks payload (manual edit?)")

    tasks_by_id, index_warnings = index_tasks_by_id(tasks)
    for warning in index_warnings:
        errors.append(warning)

    dep_state, dep_warnings = compute_dependency_state(tasks_by_id)
    for warning in dep_warnings:
        errors.append(warning)

    known_agents = load_agents_index()
    for task_id, task in tasks_by_id.items():
        status = str(task.get("status") or "TODO").strip().upper()
        if status not in ALLOWED_STATUSES:
            errors.append(f"{task_id}: invalid status {status!r}")

        title = task.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{task_id}: title must be a non-empty string")

        description = task.get("description")
        if description is not None and (not isinstance(description, str) or not description.strip()):
            errors.append(f"{task_id}: description must be a non-empty string when present")

        owner = task.get("owner")
        if owner is not None and (not isinstance(owner, str) or not owner.strip()):
            errors.append(f"{task_id}: owner must be a non-empty string when present")
        owner_upper = str(owner or "").strip().upper()
        if owner_upper and known_agents and owner_upper not in known_agents and owner_upper != "HUMAN":
            warnings.append(f"{task_id}: owner {owner_upper!r} is not a known agent id")

        tags = task.get("tags")
        if tags is not None:
            if not isinstance(tags, list) or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
                errors.append(f"{task_id}: tags must be a list of non-empty strings")

        comments = task.get("comments")
        if comments is not None:
            if not isinstance(comments, list):
                errors.append(f"{task_id}: comments must be a list")
            else:
                for idx, comment in enumerate(comments):
                    if not isinstance(comment, dict):
                        errors.append(f"{task_id}: comments[{idx}] must be an object")
                        continue
                    author = comment.get("author")
                    body = comment.get("body")
                    if not isinstance(author, str) or not author.strip():
                        errors.append(f"{task_id}: comments[{idx}].author must be a non-empty string")
                    if not isinstance(body, str) or not body.strip():
                        errors.append(f"{task_id}: comments[{idx}].body must be a non-empty string")

        verify = task.get("verify")
        if verify is not None:
            if not isinstance(verify, list) or any(not isinstance(cmd, str) or not cmd.strip() for cmd in verify):
                errors.append(f"{task_id}: verify must be a list of non-empty strings")

        dep_info = dep_state.get(task_id) or {}
        missing = dep_info.get("missing") or []
        incomplete = dep_info.get("incomplete") or []
        if status in {"DOING", "DONE"} and (missing or incomplete):
            errors.append(f"{task_id}: status {status} but dependencies are not satisfied")

        if status == "DONE":
            commit = task.get("commit")
            if not isinstance(commit, dict):
                errors.append(f"{task_id}: DONE tasks must include commit metadata")
            else:
                chash = str(commit.get("hash") or "").strip()
                msg = str(commit.get("message") or "").strip()
                if len(chash) < 7:
                    errors.append(f"{task_id}: commit.hash must be a git hash")
                if not msg:
                    errors.append(f"{task_id}: commit.message must be non-empty")

    return {"errors": sorted(set(errors)), "warnings": sorted(set(warnings))}


def cmd_task_lint(args: argparse.Namespace) -> None:
    result = lint_tasks_json()
    if not args.quiet:
        for message in result["warnings"]:
            print(f"⚠️ {message}")
    if result["errors"]:
        for message in result["errors"]:
            print(f"❌ {message}", file=sys.stderr)
        raise SystemExit(2)
    print("✅ tasks.json OK")


def cmd_ready(args: argparse.Namespace) -> None:
    ok, warnings = readiness(args.task_id)
    for warning in warnings:
        print(f"⚠️ {warning}")
    print("✅ ready" if ok else "⛔ not ready")
    raise SystemExit(0 if ok else 2)


def cmd_guard_clean(args: argparse.Namespace) -> None:
    staged = git_staged_files()
    if staged:
        for path in staged:
            print(f"❌ staged: {path}", file=sys.stderr)
        raise SystemExit(2)
    if not args.quiet:
        print("✅ index clean (no staged files)")


def cmd_guard_suggest_allow(args: argparse.Namespace) -> None:
    staged = git_staged_files()
    if not staged:
        die("No staged files", code=2)
    prefixes = suggest_allow_prefixes(staged)
    if args.format == "args":
        print(" ".join(f"--allow {p}" for p in prefixes))
        return
    for prefix in prefixes:
        print(prefix)


def cmd_guard_commit(args: argparse.Namespace) -> None:
    guard_commit_check(
        task_id=args.task_id.strip(),
        message=args.message,
        allow=list(args.allow or []),
        allow_tasks=bool(args.allow_tasks),
        require_clean=bool(args.require_clean),
        quiet=bool(args.quiet),
    )


def cmd_commit(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    message = args.message
    allow = list(args.allow or [])
    if args.auto_allow:
        allow = suggest_allow_prefixes(git_staged_files())
        if not allow:
            die("No staged files", code=2)

    guard_commit_check(
        task_id=task_id,
        message=message,
        allow=allow,
        allow_tasks=bool(args.allow_tasks),
        require_clean=bool(args.require_clean),
        quiet=bool(args.quiet),
    )

    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(ROOT),
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "git commit failed")
    commit_info = get_commit_info("HEAD")
    if not args.quiet:
        print(f"✅ committed {commit_info['hash'][:12]} {commit_info['message']}")


def cmd_start(args: argparse.Namespace) -> None:
    if not args.author or not args.body:
        die("--author and --body are required", code=2)
    if not args.force:
        require_structured_comment(args.body, prefix="Start:", min_chars=40)
    if not args.force:
        ok, warnings = readiness(args.task_id)
        if not ok:
            for warning in warnings:
                print(f"⚠️ {warning}")
            die(f"Task is not ready: {args.task_id} (use --force to override)", code=2)

    data = load_json(TASKS_PATH)
    target = _ensure_task_object(data, args.task_id)
    current = str(target.get("status") or "").strip().upper() or "TODO"
    if not is_transition_allowed(current, "DOING") and not args.force:
        die(f"Refusing status transition {current} -> DOING (use --force to override)", code=2)

    target["status"] = "DOING"
    comments = target.get("comments")
    if not isinstance(comments, list):
        comments = []
    comments.append({"author": args.author, "body": args.body})
    target["comments"] = comments
    write_tasks_json(data)
    if not args.quiet:
        print(f"✅ {args.task_id} is DOING")


def cmd_block(args: argparse.Namespace) -> None:
    if not args.author or not args.body:
        die("--author and --body are required", code=2)
    if not args.force:
        require_structured_comment(args.body, prefix="Blocked:", min_chars=40)
    data = load_json(TASKS_PATH)
    target = _ensure_task_object(data, args.task_id)
    current = str(target.get("status") or "").strip().upper() or "TODO"
    if not is_transition_allowed(current, "BLOCKED") and not args.force:
        die(f"Refusing status transition {current} -> BLOCKED (use --force to override)", code=2)
    target["status"] = "BLOCKED"
    comments = target.get("comments")
    if not isinstance(comments, list):
        comments = []
    comments.append({"author": args.author, "body": args.body})
    target["comments"] = comments
    write_tasks_json(data)
    if not args.quiet:
        print(f"✅ {args.task_id} is BLOCKED")


def cmd_task_comment(args: argparse.Namespace) -> None:
    data = load_json(TASKS_PATH)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")

    target: Optional[Dict] = None
    for task in tasks:
        if isinstance(task, dict) and task.get("id") == args.task_id:
            target = task
            break
    if not target:
        die(f"Unknown task id: {args.task_id}")

    comments = target.get("comments")
    if not isinstance(comments, list):
        comments = []
    comments.append({"author": args.author, "body": args.body})
    target["comments"] = comments

    write_tasks_json(data)


def _ensure_task_object(data: Dict, task_id: str) -> Dict:
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")
    for task in tasks:
        if isinstance(task, dict) and task.get("id") == task_id:
            return task
    die(f"Unknown task id: {task_id}")


def cmd_task_add(args: argparse.Namespace) -> None:
    data = load_json(TASKS_PATH)
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")
    task_id = args.task_id.strip()
    if any(isinstance(task, dict) and task.get("id") == task_id for task in tasks):
        die(f"Task already exists: {task_id}")
    status = (args.status or "TODO").strip().upper()
    if status not in ALLOWED_STATUSES:
        die(f"Invalid status: {status}")
    task: Dict = {
        "id": task_id,
        "title": args.title,
        "description": args.description,
        "status": status,
        "priority": args.priority,
        "owner": args.owner,
        "tags": list(dict.fromkeys((args.tag or []))),
    }
    if args.depends_on:
        task["depends_on"] = list(dict.fromkeys(args.depends_on))
    if args.verify:
        task["verify"] = list(dict.fromkeys(args.verify))
    if args.comment_author and args.comment_body:
        task["comments"] = [{"author": args.comment_author, "body": args.comment_body}]
    tasks.append(task)
    write_tasks_json(data)


def cmd_task_update(args: argparse.Namespace) -> None:
    data = load_json(TASKS_PATH)
    task = _ensure_task_object(data, args.task_id)

    if args.title is not None:
        task["title"] = args.title
    if args.description is not None:
        task["description"] = args.description
    if args.priority is not None:
        task["priority"] = args.priority
    if args.owner is not None:
        task["owner"] = args.owner

    if args.replace_tags:
        task["tags"] = []
    if args.tag:
        existing = [tag for tag in (task.get("tags") or []) if isinstance(tag, str)]
        merged = existing + args.tag
        task["tags"] = list(dict.fromkeys(tag.strip() for tag in merged if tag.strip()))

    if args.replace_depends_on:
        task["depends_on"] = []
    if args.depends_on:
        existing = [dep for dep in (task.get("depends_on") or []) if isinstance(dep, str)]
        merged = existing + args.depends_on
        task["depends_on"] = list(dict.fromkeys(dep.strip() for dep in merged if dep.strip()))

    if args.replace_verify:
        task["verify"] = []
    if args.verify:
        existing = [cmd for cmd in (task.get("verify") or []) if isinstance(cmd, str)]
        merged = existing + args.verify
        task["verify"] = list(dict.fromkeys(cmd.strip() for cmd in merged if cmd.strip()))

    write_tasks_json(data)


def _scrub_value(value: object, find_text: str, replace_text: str) -> object:
    if isinstance(value, str):
        return value.replace(find_text, replace_text)
    if isinstance(value, list):
        return [_scrub_value(item, find_text, replace_text) for item in value]
    if isinstance(value, dict):
        return {key: _scrub_value(val, find_text, replace_text) for key, val in value.items()}
    return value


def cmd_task_scrub(args: argparse.Namespace) -> None:
    find_text = args.find
    replace_text = args.replace
    if not find_text:
        die("--find must be non-empty", code=2)

    data = load_json(TASKS_PATH)
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")

    updated_tasks: List[Dict] = []
    changed_task_ids: List[str] = []
    for task in tasks:
        if not isinstance(task, dict):
            updated_tasks.append(task)
            continue
        before = json.dumps(task, ensure_ascii=False, sort_keys=True)
        after_obj = _scrub_value(task, find_text, replace_text)
        if not isinstance(after_obj, dict):
            updated_tasks.append(task)
            continue
        after = json.dumps(after_obj, ensure_ascii=False, sort_keys=True)
        updated_tasks.append(after_obj)
        if before != after:
            changed_task_ids.append(str(after_obj.get("id") or "<no-id>"))

    if args.dry_run:
        if not args.quiet:
            print(f"Would update {len(set(changed_task_ids))} task(s).")
        if changed_task_ids and not args.quiet:
            for task_id in sorted(set(changed_task_ids)):
                print(task_id)
        return

    data["tasks"] = updated_tasks
    write_tasks_json(data)
    if not args.quiet:
        print(f"Updated {len(set(changed_task_ids))} task(s).")


def run_verify_commands(task_id: str, commands: List[str], *, quiet: bool) -> None:
    for command in commands:
        if not quiet:
            print(f"$ {command}")
        result = subprocess.run(command, cwd=str(ROOT), shell=True, text=True)
        if result.returncode != 0:
            raise SystemExit(result.returncode)
    if not quiet:
        print(f"✅ verify passed for {task_id}")


def cmd_verify(args: argparse.Namespace) -> None:
    data = load_json(TASKS_PATH)
    task = _ensure_task_object(data, args.task_id)
    verify = task.get("verify")
    if verify is None:
        commands: List[str] = []
    elif isinstance(verify, list):
        commands = [cmd.strip() for cmd in verify if isinstance(cmd, str) and cmd.strip()]
    else:
        die(f"{args.task_id}: verify must be a list of strings", code=2)

    if not commands:
        if args.require:
            die(f"{args.task_id}: no verify commands configured", code=2)
        if not args.quiet:
            print(f"ℹ️ {args.task_id}: no verify commands configured")
        return

    run_verify_commands(args.task_id, commands, quiet=args.quiet)


def is_transition_allowed(current: str, nxt: str) -> bool:
    if current == nxt:
        return True
    if current == "TODO":
        return nxt in {"DOING", "BLOCKED"}
    if current == "DOING":
        return nxt in {"DONE", "BLOCKED"}
    if current == "BLOCKED":
        return nxt in {"TODO", "DOING"}
    if current == "DONE":
        return False
    return False


def cmd_task_set_status(args: argparse.Namespace) -> None:
    nxt = args.status.strip().upper()
    if nxt not in ALLOWED_STATUSES:
        die(f"Invalid status: {args.status} (allowed: {', '.join(sorted(ALLOWED_STATUSES))})")
    if nxt == "DONE" and not args.force:
        die("Use `python scripts/agentctl.py finish T-123` to mark DONE (use --force to override)", code=2)
    if (args.author and not args.body) or (args.body and not args.author):
        die("--author and --body must be provided together", code=2)

    data = load_json(TASKS_PATH)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")

    target: Optional[Dict] = None
    for task in tasks:
        if isinstance(task, dict) and task.get("id") == args.task_id:
            target = task
            break
    if not target:
        die(f"Unknown task id: {args.task_id}")

    current = str(target.get("status") or "").strip().upper() or "TODO"
    if not is_transition_allowed(current, nxt) and not args.force:
        die(f"Refusing status transition {current} -> {nxt} (use --force to override)")

    if nxt in {"DOING", "DONE"} and not args.force:
        ok, warnings = readiness(args.task_id)
        if not ok:
            for warning in warnings:
                print(f"⚠️ {warning}")
            die(f"Task is not ready: {args.task_id} (use --force to override)", code=2)

    target["status"] = nxt

    if args.author and args.body:
        comments = target.get("comments")
        if not isinstance(comments, list):
            comments = []
        comments.append({"author": args.author, "body": args.body})
        target["comments"] = comments

    if args.commit:
        commit_info = get_commit_info(args.commit)
        target["commit"] = commit_info

    write_tasks_json(data)


def cmd_finish(args: argparse.Namespace) -> None:
    if (args.author and not args.body) or (args.body and not args.author):
        die("--author and --body must be provided together", code=2)
    if args.author and args.body and not args.force:
        require_structured_comment(args.body, prefix="Verified:", min_chars=60)

    lint = lint_tasks_json()
    if lint["warnings"] and not args.quiet:
        for message in lint["warnings"]:
            print(f"⚠️ {message}")
    if lint["errors"] and not args.force:
        for message in lint["errors"]:
            print(f"❌ {message}", file=sys.stderr)
        die("tasks.json failed lint (use --force to override)", code=2)

    ok, warnings = readiness(args.task_id)
    if not ok and not args.force:
        for warning in warnings:
            print(f"⚠️ {warning}")
        die(f"Task is not ready: {args.task_id} (use --force to override)", code=2)

    commit_info = get_commit_info(args.commit)
    if args.require_task_id_in_commit and args.task_id not in commit_info.get("message", "") and not args.force:
        die(
            f"Commit subject does not mention {args.task_id}: {commit_info.get('message')!r} "
            "(use --force or --no-require-task-id-in-commit)"
        )

    data = load_json(TASKS_PATH)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")

    target = _ensure_task_object(data, args.task_id)

    verify = target.get("verify")
    if verify is None:
        commands: List[str] = []
    elif isinstance(verify, list):
        commands = [cmd.strip() for cmd in verify if isinstance(cmd, str) and cmd.strip()]
    else:
        if not args.force:
            die(f"{args.task_id}: verify must be a list of strings (use --force to override)", code=2)
        commands = []
    if commands and not args.skip_verify and not args.force:
        run_verify_commands(args.task_id, commands, quiet=args.quiet)

    target["status"] = "DONE"
    target["commit"] = commit_info

    if args.author and args.body:
        comments = target.get("comments")
        if not isinstance(comments, list):
            comments = []
        comments.append({"author": args.author, "body": args.body})
        target["comments"] = comments

    write_tasks_json(data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agentctl", description="TokenSpot agent workflow helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_quickstart = sub.add_parser("quickstart", help="Print agentctl usage quick reference (.codex-swarm/agentctl.md)")
    p_quickstart.set_defaults(func=cmd_quickstart)

    p_agents = sub.add_parser("agents", help="List registered agents under .codex-swarm/agents/")
    p_agents.set_defaults(func=cmd_agents)

    p_ready = sub.add_parser("ready", help="Check if a task is ready to start (dependencies DONE)")
    p_ready.add_argument("task_id")
    p_ready.set_defaults(func=cmd_ready)

    p_verify = sub.add_parser("verify", help="Run verify commands declared on a task (tasks.json)")
    p_verify.add_argument("task_id")
    p_verify.add_argument("--quiet", action="store_true", help="Minimal output")
    p_verify.add_argument("--require", action="store_true", help="Fail if no verify commands exist")
    p_verify.set_defaults(func=cmd_verify)

    p_guard = sub.add_parser("guard", help="Guardrails for git staging/commit hygiene")
    guard_sub = p_guard.add_subparsers(dest="guard_cmd", required=True)

    p_guard_clean = guard_sub.add_parser("clean", help="Fail if there are staged files")
    p_guard_clean.add_argument("--quiet", action="store_true", help="Minimal output")
    p_guard_clean.set_defaults(func=cmd_guard_clean)

    p_guard_suggest = guard_sub.add_parser("suggest-allow", help="Suggest minimal --allow prefixes for staged files")
    p_guard_suggest.add_argument("--format", choices=["lines", "args"], default="lines", help="Output format")
    p_guard_suggest.set_defaults(func=cmd_guard_suggest_allow)

    p_guard_commit = guard_sub.add_parser("commit", help="Validate staged files and planned commit message")
    p_guard_commit.add_argument("task_id", help="Active task id (must appear in --message)")
    p_guard_commit.add_argument("--message", "-m", required=True, help="Planned commit message")
    p_guard_commit.add_argument("--allow", action="append", help="Allowed path prefix (repeatable)")
    p_guard_commit.add_argument("--allow-tasks", action="store_true", help="Allow staging tasks.json")
    p_guard_commit.add_argument("--allow-dirty", action="store_true", help="Deprecated (unstaged changes are allowed by default)")
    p_guard_commit.add_argument("--require-clean", action="store_true", help="Fail if there are unstaged changes")
    p_guard_commit.add_argument("--quiet", action="store_true", help="Minimal output")
    p_guard_commit.set_defaults(func=cmd_guard_commit)

    p_commit = sub.add_parser("commit", help="Run guard commit checks, then `git commit`")
    p_commit.add_argument("task_id", help="Active task id (must appear in --message)")
    p_commit.add_argument("--message", "-m", required=True, help="Commit message")
    p_commit.add_argument("--allow", action="append", help="Allowed path prefix (repeatable)")
    p_commit.add_argument("--auto-allow", action="store_true", help="Derive --allow prefixes from staged files")
    p_commit.add_argument("--allow-tasks", action="store_true", help="Allow staging tasks.json")
    p_commit.add_argument("--require-clean", action="store_true", help="Fail if there are unstaged changes")
    p_commit.add_argument("--quiet", action="store_true", help="Minimal output")
    p_commit.set_defaults(func=cmd_commit)

    p_start = sub.add_parser("start", help="Mark task DOING with a mandatory comment")
    p_start.add_argument("task_id")
    p_start.add_argument("--author", required=True)
    p_start.add_argument("--body", required=True)
    p_start.add_argument("--quiet", action="store_true", help="Minimal output")
    p_start.add_argument("--force", action="store_true", help="Bypass readiness/transition checks")
    p_start.set_defaults(func=cmd_start)

    p_block = sub.add_parser("block", help="Mark task BLOCKED with a mandatory comment")
    p_block.add_argument("task_id")
    p_block.add_argument("--author", required=True)
    p_block.add_argument("--body", required=True)
    p_block.add_argument("--quiet", action="store_true", help="Minimal output")
    p_block.add_argument("--force", action="store_true", help="Bypass transition checks")
    p_block.set_defaults(func=cmd_block)

    p_task = sub.add_parser("task", help="Operate on tasks.json")
    task_sub = p_task.add_subparsers(dest="task_cmd", required=True)

    p_lint = task_sub.add_parser("lint", help="Validate tasks.json (schema, deps, checksum)")
    p_lint.add_argument("--quiet", action="store_true", help="Suppress warnings")
    p_lint.set_defaults(func=cmd_task_lint)

    p_add = task_sub.add_parser("add", help="Add a new task to tasks.json (no manual edits)")
    p_add.add_argument("task_id")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--description", required=True)
    p_add.add_argument("--status", default="TODO", help="Default: TODO")
    p_add.add_argument("--priority", required=True)
    p_add.add_argument("--owner", required=True)
    p_add.add_argument("--tag", action="append", help="Repeatable")
    p_add.add_argument("--depends-on", action="append", dest="depends_on", help="Repeatable")
    p_add.add_argument("--verify", action="append", help="Repeatable: shell command")
    p_add.add_argument("--comment-author", dest="comment_author")
    p_add.add_argument("--comment-body", dest="comment_body")
    p_add.set_defaults(func=cmd_task_add)

    p_update = task_sub.add_parser("update", help="Update a task in tasks.json (no manual edits)")
    p_update.add_argument("task_id")
    p_update.add_argument("--title")
    p_update.add_argument("--description")
    p_update.add_argument("--priority")
    p_update.add_argument("--owner")
    p_update.add_argument("--tag", action="append", help="Repeatable (append)")
    p_update.add_argument("--replace-tags", action="store_true")
    p_update.add_argument("--depends-on", action="append", dest="depends_on", help="Repeatable (append)")
    p_update.add_argument("--replace-depends-on", action="store_true")
    p_update.add_argument("--verify", action="append", help="Repeatable (append)")
    p_update.add_argument("--replace-verify", action="store_true")
    p_update.set_defaults(func=cmd_task_update)

    p_scrub = task_sub.add_parser("scrub", help="Replace text across tasks.json task fields")
    p_scrub.add_argument("--find", required=True, help="Substring to replace (required)")
    p_scrub.add_argument("--replace", default="", help="Replacement (default: empty)")
    p_scrub.add_argument("--dry-run", action="store_true", help="Print affected task ids without writing")
    p_scrub.add_argument("--quiet", action="store_true", help="Minimal output")
    p_scrub.set_defaults(func=cmd_task_scrub)

    p_list = task_sub.add_parser("list", help="List tasks from tasks.json")
    p_list.add_argument("--status", action="append", help="Filter by status (repeatable)")
    p_list.add_argument("--owner", action="append", help="Filter by owner (repeatable)")
    p_list.add_argument("--tag", action="append", help="Filter by tag (repeatable)")
    p_list.add_argument("--quiet", action="store_true", help="Suppress warnings")
    p_list.set_defaults(func=cmd_task_list)

    p_next = task_sub.add_parser("next", help="List tasks ready to start (dependencies DONE)")
    p_next.add_argument("--status", action="append", help="Filter by status (repeatable, default: TODO)")
    p_next.add_argument("--owner", action="append", help="Filter by owner (repeatable)")
    p_next.add_argument("--tag", action="append", help="Filter by tag (repeatable)")
    p_next.add_argument("--limit", type=int, help="Limit number of results")
    p_next.add_argument("--quiet", action="store_true", help="Suppress warnings")
    p_next.set_defaults(func=cmd_task_next)

    p_show = task_sub.add_parser("show", help="Show a single task from tasks.json")
    p_show.add_argument("task_id")
    p_show.add_argument("--last-comments", type=int, default=5, help="How many latest comments to print")
    p_show.add_argument("--quiet", action="store_true", help="Suppress warnings")
    p_show.set_defaults(func=cmd_task_show)

    p_search = task_sub.add_parser("search", help="Search tasks by text (title/description/tags/comments)")
    p_search.add_argument("query")
    p_search.add_argument("--regex", action="store_true", help="Treat query as a case-insensitive regex")
    p_search.add_argument("--status", action="append", help="Filter by status (repeatable)")
    p_search.add_argument("--owner", action="append", help="Filter by owner (repeatable)")
    p_search.add_argument("--tag", action="append", help="Filter by tag (repeatable)")
    p_search.add_argument("--limit", type=int, help="Limit number of results")
    p_search.add_argument("--quiet", action="store_true", help="Suppress warnings")
    p_search.set_defaults(func=cmd_task_search)

    p_scaffold = task_sub.add_parser("scaffold", help="Create docs/workflow/T-###.md skeleton for a task")
    p_scaffold.add_argument("task_id")
    p_scaffold.add_argument("--title", help="Optional title override")
    p_scaffold.add_argument("--overwrite", action="store_true", help="Overwrite if the file exists")
    p_scaffold.add_argument("--force", action="store_true", help="Allow scaffolding even if task id is unknown")
    p_scaffold.add_argument("--quiet", action="store_true", help="Minimal output")
    p_scaffold.set_defaults(func=cmd_task_scaffold)

    p_comment = task_sub.add_parser("comment", help="Append a comment to a task")
    p_comment.add_argument("task_id")
    p_comment.add_argument("--author", required=True)
    p_comment.add_argument("--body", required=True)
    p_comment.set_defaults(func=cmd_task_comment)

    p_status = task_sub.add_parser("set-status", help="Update task status with readiness checks")
    p_status.add_argument("task_id")
    p_status.add_argument("status", help="TODO|DOING|BLOCKED|DONE")
    p_status.add_argument("--author", help="Optional comment author (requires --body)")
    p_status.add_argument("--body", help="Optional comment body (requires --author)")
    p_status.add_argument("--commit", help="Attach commit metadata from a git rev (e.g., HEAD)")
    p_status.add_argument("--force", action="store_true", help="Bypass transition and readiness checks")
    p_status.set_defaults(func=cmd_task_set_status)

    p_finish = sub.add_parser(
        "finish",
        help="Mark task DONE + attach commit metadata (typically after a code commit)",
    )
    p_finish.add_argument("task_id")
    p_finish.add_argument("--commit", default="HEAD", help="Git rev to attach as task commit metadata (default: HEAD)")
    p_finish.add_argument("--author", help="Optional comment author (requires --body)")
    p_finish.add_argument("--body", help="Optional comment body (requires --author)")
    p_finish.add_argument("--skip-verify", action="store_true", help="Do not run verify even if configured")
    p_finish.add_argument("--quiet", action="store_true", help="Minimal output")
    p_finish.add_argument("--force", action="store_true", help="Bypass readiness and commit-subject checks")
    p_finish.add_argument(
        "--no-require-task-id-in-commit",
        dest="require_task_id_in_commit",
        action="store_false",
        help="Allow finishing even if commit subject does not mention the task id",
    )
    p_finish.set_defaults(require_task_id_in_commit=True, func=cmd_finish)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if not func:
        parser.print_help()
        raise SystemExit(2)
    func(args)


if __name__ == "__main__":
    main()
