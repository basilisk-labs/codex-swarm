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
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SWARM_DIR = ROOT / ".codex-swarm"
SWARM_CONFIG_PATH = SWARM_DIR / "swarm.config.json"

ALLOWED_WORKFLOW_MODES: Set[str] = {"direct", "branch_pr"}
DEFAULT_WORKFLOW_MODE = "direct"

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


def git_toplevel(*, cwd: Path = ROOT) -> Path:
    try:
        result = run(["git", "rev-parse", "--show-toplevel"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to resolve git toplevel")
    raw = (result.stdout or "").strip()
    if not raw:
        die("Failed to resolve git toplevel")
    return Path(raw).resolve()


def git_current_branch(*, cwd: Path = ROOT) -> str:
    try:
        result = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to resolve git branch")
    return (result.stdout or "").strip()


def is_task_worktree_checkout(*, cwd: Path = ROOT) -> bool:
    top = git_toplevel(cwd=cwd)
    parts = top.parts
    for idx in range(len(parts) - 1):
        if parts[idx] == ".codex-swarm" and parts[idx + 1] == "worktrees":
            return True
    return False


def ensure_git_clean(*, cwd: Path = ROOT, action: str) -> None:
    try:
        result = run(["git", "status", "--porcelain"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to read git status")
    if (result.stdout or "").strip():
        dirty = (result.stdout or "").strip()
        die(
            "\n".join(
                [
                    f"Refusing {action}: working tree is dirty (commit/stash changes first)",
                    "Fix:",
                    "  1) `git status --porcelain` (review changes)",
                    "  2) Commit/stash/reset until clean",
                    "  3) Re-run the command",
                    "Dirty paths:",
                    *[f"  {line}" for line in dirty.splitlines()],
                    f"Context: {format_command_context(cwd=Path.cwd().resolve())}",
                ]
            ),
            code=2,
        )


def git_status_porcelain(*, cwd: Path) -> str:
    try:
        result = run(["git", "status", "--porcelain"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to read git status")
    return (result.stdout or "").strip()


def ensure_path_ignored(path: str, *, cwd: Path = ROOT) -> None:
    target = str(path).strip()
    if not target:
        die("Missing ignore target", code=2)
    try:
        proc = run(["git", "check-ignore", "-q", target], cwd=cwd, check=False)
    except subprocess.CalledProcessError:
        proc = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
    if proc.returncode != 0:
        die(
            "\n".join(
                [
                    f"Refusing operation: {target!r} is not ignored by git",
                    "Fix:",
                    f"  1) Add `{target}` to `.gitignore`",
                    "  2) Re-run the command",
                    f"Context: branch={git_current_branch(cwd=cwd)!r} cwd={Path.cwd().resolve()}",
                ]
            ),
            code=2,
        )


def format_command_context(*, cwd: Path) -> str:
    repo_root = git_toplevel(cwd=cwd)
    cwd_resolved = cwd.resolve()
    rel = str(cwd_resolved.relative_to(repo_root)) if cwd_resolved != repo_root else "."
    return f"repo_root={repo_root} cwd={rel} branch={git_current_branch(cwd=cwd)!r} workflow_mode={workflow_mode()!r}"


def print_block(label: str, text: str) -> None:
    print(f"{label}: {text}".rstrip())


def ensure_invoked_from_repo_root(*, action: str) -> None:
    cwd = Path.cwd().resolve()
    if cwd != ROOT.resolve():
        die(
            "\n".join(
                [
                    f"Refusing {action}: command must be run from the repo root directory",
                    "Fix:",
                    f"  1) `cd {ROOT}`",
                    "  2) Re-run the command",
                    f"Context: {format_command_context(cwd=cwd)}",
                ]
            ),
            code=2,
        )


def require_not_task_worktree(*, cwd: Path = ROOT, action: str) -> None:
    if is_task_worktree_checkout(cwd=cwd):
        die(
            "\n".join(
                [
                    f"Refusing {action}: run from the repo root checkout (not from .codex-swarm/worktrees/*)",
                    "Fix:",
                    f"  1) `cd {ROOT}`",
                    "  2) Ensure you're on `main` (if required)",
                    "  3) Re-run the command",
                    f"Context: {format_command_context(cwd=Path.cwd().resolve())}",
                ]
            ),
            code=2,
        )


def require_branch(name: str, *, cwd: Path = ROOT, action: str) -> None:
    current = git_current_branch(cwd=cwd)
    if current != name:
        die(
            "\n".join(
                [
                    f"Refusing {action}: must be on {name!r} (current: {current!r})",
                    "Fix:",
                    f"  1) `git checkout {name}`",
                    "  2) Ensure working tree is clean",
                    "  3) Re-run the command",
                    f"Context: {format_command_context(cwd=Path.cwd().resolve())}",
                ]
            ),
            code=2,
        )


def require_tasks_json_write_context(*, cwd: Path = ROOT, force: bool = False) -> None:
    if force:
        return
    if is_task_worktree_checkout(cwd=cwd):
        require_not_task_worktree(cwd=cwd, action="tasks.json write")
    if is_branch_pr_mode():
        require_branch(DEFAULT_MAIN_BRANCH, cwd=cwd, action="tasks.json write")


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def normalize_slug(value: str) -> str:
    raw = (value or "").strip().lower()
    raw = raw.replace("_", "-").replace(" ", "-")
    raw = _SLUG_RE.sub("-", raw).strip("-")
    return raw or "work"


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


def workflow_mode() -> str:
    raw = str(_SWARM_CONFIG.get("workflow_mode") or "").strip() or DEFAULT_WORKFLOW_MODE
    if raw not in ALLOWED_WORKFLOW_MODES:
        die(
            f"Invalid workflow_mode in {SWARM_CONFIG_PATH}: {raw!r} "
            f"(allowed: {', '.join(sorted(ALLOWED_WORKFLOW_MODES))})",
            code=2,
        )
    return raw


def is_branch_pr_mode() -> bool:
    return workflow_mode() == "branch_pr"

DEFAULT_MAIN_BRANCH = "main"
WORKTREES_DIRNAME = str(Path(".codex-swarm") / "worktrees")
WORKTREES_DIR = SWARM_DIR / "worktrees"
# Legacy PR artifacts directory (pre per-task layout).
PRS_DIR = WORKFLOW_DIR / "prs"


def now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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

    target = workflow_task_readme_path(task_id)
    legacy = legacy_workflow_task_doc_path(task_id)
    if legacy.exists() and not args.overwrite:
        die(f"Legacy task doc exists: {legacy} (migrate it to {target} or re-run with --overwrite)", code=2)
    if target.exists() and not args.overwrite:
        die(f"File already exists: {target}", code=2)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(task_readme_template(task_id), encoding="utf-8")
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


def get_commit_info(rev: str, *, cwd: Path = ROOT) -> Dict[str, str]:
    try:
        result = run(["git", "show", "-s", "--pretty=format:%H\x1f%s", rev], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or f"Failed to resolve git revision: {rev}")
    raw = (result.stdout or "").strip()
    if "\x1f" not in raw:
        die(f"Unexpected git output for rev {rev}")
    commit_hash, subject = raw.split("\x1f", 1)
    return {"hash": commit_hash.strip(), "message": subject.strip()}


def git_staged_files(*, cwd: Path) -> List[str]:
    try:
        result = run(["git", "diff", "--name-only", "--cached"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to read staged files")
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def git_unstaged_files(*, cwd: Path) -> List[str]:
    try:
        result = run(["git", "diff", "--name-only"], cwd=cwd, check=True)
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


_TASK_BRANCH_RE = re.compile(r"^task/(T-[0-9]{3,})/[^/]+$")
_VERIFIED_SHA_RE = re.compile(r"verified_sha=([0-9a-f]{7,40})", re.IGNORECASE)


def parse_task_id_from_task_branch(branch: str) -> Optional[str]:
    raw = (branch or "").strip()
    match = _TASK_BRANCH_RE.match(raw)
    if not match:
        return None
    return match.group(1)


def extract_last_verified_sha_from_log(text: str) -> Optional[str]:
    for raw_line in reversed((text or "").splitlines()):
        match = _VERIFIED_SHA_RE.search(raw_line)
        if match:
            return match.group(1)
    return None


def guard_commit_check(
    *,
    task_id: str,
    message: str,
    allow: List[str],
    allow_tasks: bool,
    require_clean: bool,
    quiet: bool,
    cwd: Path,
) -> None:
    if task_id not in message:
        die(f"Commit message must include {task_id}", code=2)
    if not commit_message_has_meaningful_summary(task_id, message):
        die(
            "Commit message is too generic; include a short summary (and constraints when relevant), "
            'e.g. "✨ T-123 Add X (no network)"',
            code=2,
        )

    staged = git_staged_files(cwd=cwd)
    if not staged:
        die("No staged files", code=2)

    current_branch = git_current_branch(cwd=cwd)
    if is_branch_pr_mode():
        if "tasks.json" in staged and not allow_tasks:
            die(
                "\n".join(
                    [
                        "Refusing commit: tasks.json is forbidden in workflow_mode='branch_pr'",
                        "Fix:",
                        "  1) Remove tasks.json from the index (`git restore --staged tasks.json`)",
                        "  2) Commit code/docs/PR artifacts on the task branch",
                        "  3) Close the task on main via INTEGRATOR (tasks.json only in closure commit)",
                        f"Context: {format_command_context(cwd=cwd)}",
                    ]
                ),
                code=2,
            )
        if "tasks.json" in staged and allow_tasks:
            if is_task_worktree_checkout(cwd=cwd):
                die(
                    f"Refusing commit: tasks.json from a worktree checkout (.codex-swarm/worktrees/*)\nContext: {format_command_context(cwd=cwd)}",
                    code=2,
                )
            if current_branch != DEFAULT_MAIN_BRANCH:
                die(
                    f"Refusing commit: tasks.json allowed only on {DEFAULT_MAIN_BRANCH!r} in branch_pr mode\n"
                    f"Context: {format_command_context(cwd=cwd)}",
                    code=2,
                )
        if not allow_tasks:
            if current_branch != DEFAULT_MAIN_BRANCH:
                parsed = parse_task_id_from_task_branch(current_branch)
                if parsed != task_id:
                    die(
                        "\n".join(
                            [
                                f"Refusing commit: branch {current_branch!r} does not match task {task_id}",
                                "Fix:",
                                f"  1) Switch to `task/{task_id}/<slug>`",
                                f"  2) Re-run `python scripts/agentctl.py guard commit {task_id} ...`",
                                f"Context: {format_command_context(cwd=cwd)}",
                            ]
                        ),
                        code=2,
                    )

    if not allow:
        die("Provide at least one --allow <path> prefix", code=2)

    unstaged = git_unstaged_files(cwd=cwd)
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
        if owner_upper and known_agents and owner_upper not in known_agents and owner_upper not in {"HUMAN", "ORCHESTRATOR"}:
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
    staged = git_staged_files(cwd=Path.cwd().resolve())
    if staged:
        for path in staged:
            print(f"❌ staged: {path}", file=sys.stderr)
        raise SystemExit(2)
    if not args.quiet:
        print("✅ index clean (no staged files)")


def cmd_guard_suggest_allow(args: argparse.Namespace) -> None:
    staged = git_staged_files(cwd=Path.cwd().resolve())
    if not staged:
        die("No staged files", code=2)
    prefixes = suggest_allow_prefixes(staged)
    if args.format == "args":
        print(" ".join(f"--allow {p}" for p in prefixes))
        return
    for prefix in prefixes:
        print(prefix)


def cmd_guard_commit(args: argparse.Namespace) -> None:
    cwd = Path.cwd().resolve()
    allow = list(args.allow or [])
    if args.auto_allow and not allow:
        allow = suggest_allow_prefixes(git_staged_files(cwd=cwd))
        if not allow:
            die("No staged files", code=2)
    guard_commit_check(
        task_id=args.task_id.strip(),
        message=args.message,
        allow=allow,
        allow_tasks=bool(args.allow_tasks),
        require_clean=bool(args.require_clean),
        quiet=bool(args.quiet),
        cwd=cwd,
    )


def cmd_commit(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    message = args.message
    allow = list(args.allow or [])
    cwd = Path.cwd().resolve()
    if args.auto_allow:
        allow = suggest_allow_prefixes(git_staged_files(cwd=cwd))
        if not allow:
            die("No staged files", code=2)

    guard_commit_check(
        task_id=task_id,
        message=message,
        allow=allow,
        allow_tasks=bool(args.allow_tasks),
        require_clean=bool(args.require_clean),
        quiet=bool(args.quiet),
        cwd=cwd,
    )

    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(cwd),
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "git commit failed")
    commit_info = get_commit_info("HEAD", cwd=cwd)
    if not args.quiet:
        print(f"✅ committed {commit_info['hash'][:12]} {commit_info['message']}")


def cmd_start(args: argparse.Namespace) -> None:
    if not args.author or not args.body:
        die("--author and --body are required", code=2)
    require_tasks_json_write_context(force=bool(args.force))
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
    require_tasks_json_write_context(force=bool(args.force))
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
    require_tasks_json_write_context()
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
    require_tasks_json_write_context()
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
        "depends_on": list(dict.fromkeys((args.depends_on or []))),
    }
    if args.verify:
        task["verify"] = list(dict.fromkeys(args.verify))
    if args.comment_author and args.comment_body:
        task["comments"] = [{"author": args.comment_author, "body": args.comment_body}]
    tasks.append(task)
    write_tasks_json(data)


def cmd_task_update(args: argparse.Namespace) -> None:
    require_tasks_json_write_context()
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

    require_tasks_json_write_context()
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


def cmd_verify(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    commands = get_task_verify_commands_for(task_id)

    if not commands:
        if args.require:
            die(f"{task_id}: no verify commands configured", code=2)
        if not args.quiet:
            print(f"ℹ️ {task_id}: no verify commands configured")
        return

    cwd = Path(args.cwd).resolve() if args.cwd else ROOT
    if ROOT.resolve() not in cwd.parents and cwd.resolve() != ROOT.resolve():
        die(f"--cwd must stay under repo root: {cwd}", code=2)

    log_path: Optional[Path] = None
    if getattr(args, "log", None):
        log_path = Path(str(args.log)).resolve()
    else:
        # Convenience default: if a tracked PR artifact exists, write into its verify.log.
        pr_root = pr_dir(task_id)
        legacy_pr_root = legacy_pr_dir(task_id)
        if pr_root.exists():
            log_path = (pr_root / "verify.log").resolve()
        elif legacy_pr_root.exists():
            log_path = (legacy_pr_root / "verify.log").resolve()

    if log_path:
        if ROOT.resolve() not in log_path.parents and log_path.resolve() != ROOT.resolve():
            die(f"--log must stay under repo root: {log_path}", code=2)

    pr_meta_path_new = pr_dir(task_id) / "meta.json"
    pr_meta_path_legacy = legacy_pr_dir(task_id) / "meta.json"
    pr_meta_path = pr_meta_path_new if pr_meta_path_new.exists() else pr_meta_path_legacy
    pr_meta: Optional[Dict] = pr_load_meta(pr_meta_path) if pr_meta_path.exists() else None

    head_sha = git_rev_parse("HEAD", cwd=cwd)
    current_sha = head_sha
    if log_path and pr_meta:
        log_parent_chain = log_path.resolve().parents
        pr_roots = [pr_dir(task_id).resolve(), legacy_pr_dir(task_id).resolve()]
        if any(root in log_parent_chain for root in pr_roots):
            meta_head = str(pr_meta.get("head_sha") or "").strip()
            if meta_head:
                current_sha = meta_head
                if meta_head != head_sha and not args.quiet:
                    print(
                        f"⚠️ {task_id}: PR meta head_sha differs from HEAD; run `python scripts/agentctl.py pr update {task_id}` if needed"
                    )

    if getattr(args, "skip_if_unchanged", False):
        if git_status_porcelain(cwd=cwd):
            if not args.quiet:
                print(f"⚠️ {task_id}: working tree is dirty; ignoring --skip-if-unchanged")
        else:
            last_verified_sha: Optional[str] = None
            if pr_meta:
                last_verified_sha = str(pr_meta.get("last_verified_sha") or "").strip() or None
            if not last_verified_sha and log_path and log_path.exists():
                last_verified_sha = extract_last_verified_sha_from_log(
                    log_path.read_text(encoding="utf-8", errors="replace")
                )
            if last_verified_sha and last_verified_sha == current_sha:
                timestamp = now_iso_utc()
                header = f"[{timestamp}] ℹ️ skipped (unchanged verified_sha={current_sha})"
                if log_path:
                    append_verify_log(log_path, header=header, content="")
                if not args.quiet:
                    print(f"ℹ️ {task_id}: verify skipped (unchanged sha {current_sha[:12]})")
                return

    run_verify_with_capture(task_id, cwd=cwd, quiet=bool(args.quiet), log_path=log_path, current_sha=current_sha)

    if pr_meta_path.exists():
        pr_meta_write = pr_load_meta(pr_meta_path)
        pr_meta_write["last_verified_sha"] = current_sha
        pr_meta_write["last_verified_at"] = now_iso_utc()
        pr_write_meta(pr_meta_path, pr_meta_write)


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

    require_tasks_json_write_context(force=bool(args.force))
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
    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)
    if (args.author and not args.body) or (args.body and not args.author):
        die("--author and --body must be provided together", code=2)
    require_tasks_json_write_context(force=bool(args.force))
    pr_path: Optional[Path] = None
    pr_branch: str = ""
    pr_base: str = ""
    pr_meta: Dict = {}
    if is_branch_pr_mode() and not args.force:
        ensure_git_clean(action="finish")
        if not args.author or not args.body:
            die("--author and --body are required in workflow_mode='branch_pr'", code=2)
        if str(args.author).strip().upper() != "INTEGRATOR":
            die("--author must be INTEGRATOR in workflow_mode='branch_pr'", code=2)
        pr_path = pr_dir_any(task_id)
        if not pr_path.exists():
            die(f"Missing PR artifact dir: {pr_path} (required for finish in branch_pr mode)", code=2)
        pr_meta = pr_load_meta(pr_path / "meta.json")
        pr_branch = str(pr_meta.get("branch") or "").strip()
        pr_base = str(pr_meta.get("base_branch") or DEFAULT_MAIN_BRANCH).strip()
        pr_check(task_id, branch=pr_branch or None, base=pr_base or None, quiet=True)
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

    ok, warnings = readiness(task_id)
    if not ok and not args.force:
        for warning in warnings:
            print(f"⚠️ {warning}")
        die(f"Task is not ready: {task_id} (use --force to override)", code=2)

    commit_info = get_commit_info(args.commit)
    if args.require_task_id_in_commit and task_id not in commit_info.get("message", "") and not args.force:
        die(
            f"Commit subject does not mention {task_id}: {commit_info.get('message')!r} "
            "(use --force or --no-require-task-id-in-commit)"
        )

    data = load_json(TASKS_PATH)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        die("tasks.json must contain a top-level 'tasks' list")

    target = _ensure_task_object(data, task_id)

    verify = target.get("verify")
    if verify is None:
        commands: List[str] = []
    elif isinstance(verify, list):
        commands = [cmd.strip() for cmd in verify if isinstance(cmd, str) and cmd.strip()]
    else:
        if not args.force:
            die(f"{task_id}: verify must be a list of strings (use --force to override)", code=2)
        commands = []
    if commands and not args.skip_verify and not args.force:
        run_verify_commands(task_id, commands, cwd=ROOT, quiet=args.quiet)

    target["status"] = "DONE"
    target["commit"] = commit_info

    if pr_path and is_branch_pr_mode() and not args.force:
        review_path = pr_path / "review.md"
        if review_path.exists():
            notes = parse_handoff_notes(review_path.read_text(encoding="utf-8", errors="replace"))
            if notes:
                digest = hashlib.sha256(
                    ("\n".join(f"{n['author']}:{n['body']}" for n in notes)).encode("utf-8")
                ).hexdigest()
                applied = str(pr_meta.get("handoff_applied_digest") or "").strip()
                if digest != applied:
                    comments = target.get("comments")
                    if not isinstance(comments, list):
                        comments = []
                    for note in notes:
                        comments.append({"author": note["author"], "body": note["body"]})
                    target["comments"] = comments
                    pr_meta["handoff_applied_digest"] = digest
                    pr_meta["handoff_applied_at"] = now_iso_utc()
                    pr_write_meta(pr_path / "meta.json", pr_meta)
        now = now_iso_utc()
        pr_meta.setdefault("merged_at", now)
        pr_meta.setdefault("merge_commit", commit_info.get("hash"))
        pr_meta.setdefault("closed_at", now)
        pr_meta["close_commit"] = commit_info.get("hash")
        pr_meta["status"] = pr_meta.get("status") or "CLOSED"
        if str(pr_meta.get("status")).strip().upper() != "CLOSED":
            pr_meta["status"] = "CLOSED"
        pr_meta["updated_at"] = now
        pr_write_meta(pr_path / "meta.json", pr_meta)

    if args.author and args.body:
        comments = target.get("comments")
        if not isinstance(comments, list):
            comments = []
        comments.append({"author": args.author, "body": args.body})
        target["comments"] = comments

    write_tasks_json(data)


def git_rev_parse(rev: str, *, cwd: Path = ROOT) -> str:
    try:
        result = run(["git", "rev-parse", rev], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or f"Failed to resolve git rev: {rev}")
    return (result.stdout or "").strip()


def git_branch_exists(branch: str, *, cwd: Path = ROOT) -> bool:
    try:
        run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"], cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def git_diff_names(base: str, head: str, *, cwd: Path = ROOT) -> List[str]:
    try:
        result = run(["git", "diff", "--name-only", f"{base}...{head}"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to compute git diff")
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def git_diff_stat(base: str, head: str, *, cwd: Path = ROOT) -> str:
    try:
        result = run(["git", "diff", "--stat", f"{base}...{head}"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to compute git diffstat")
    return (result.stdout or "").rstrip() + "\n"


def git_log_subjects(base: str, head: str, *, cwd: Path = ROOT, limit: int = 50) -> List[str]:
    try:
        result = run(
            ["git", "log", f"--max-count={limit}", "--pretty=format:%s", f"{base}..{head}"],
            cwd=cwd,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to read git log")
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def git_show_text(rev: str, relpath: str, *, cwd: Path = ROOT) -> Optional[str]:
    rel = str(relpath or "").strip().lstrip("/")
    if not rel:
        return None
    try:
        proc = run(["git", "show", f"{rev}:{rel}"], cwd=cwd, check=False)
    except subprocess.CalledProcessError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def git_worktree_list_porcelain(*, cwd: Path = ROOT) -> str:
    try:
        result = run(["git", "worktree", "list", "--porcelain"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to list git worktrees")
    return (result.stdout or "")


def parse_git_worktrees_porcelain(text: str) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    current: Dict[str, str] = {}
    for raw_line in (text or "").splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if current:
                entries.append(current)
                current = {}
            continue
        if " " not in line:
            continue
        key, value = line.split(" ", 1)
        current[key.strip()] = value.strip()
    if current:
        entries.append(current)
    return entries


def detect_worktree_path_for_branch(branch: str, *, cwd: Path = ROOT) -> Optional[Path]:
    want = (branch or "").strip()
    if not want:
        return None
    entries = parse_git_worktrees_porcelain(git_worktree_list_porcelain(cwd=cwd))
    for entry in entries:
        wt_path = entry.get("worktree")
        ref = entry.get("branch")  # refs/heads/<branch>
        if not wt_path or not ref:
            continue
        if ref == f"refs/heads/{want}":
            return Path(wt_path).resolve()
    return None


def detect_branch_for_worktree_path(path: Path, *, cwd: Path = ROOT) -> Optional[str]:
    entries = parse_git_worktrees_porcelain(git_worktree_list_porcelain(cwd=cwd))
    want = path.resolve()
    for entry in entries:
        wt_path = entry.get("worktree")
        ref = entry.get("branch")
        if not wt_path or not ref:
            continue
        if Path(wt_path).resolve() == want and ref.startswith("refs/heads/"):
            return ref[len("refs/heads/") :]
    return None


def assert_no_diff_paths(*, base: str, branch: str, forbidden: List[str], cwd: Path = ROOT) -> None:
    changed = set(git_diff_names(base, branch, cwd=cwd))
    bad = [p for p in forbidden if p in changed]
    if bad:
        die(
            "\n".join(
                [
                    f"Refusing operation: branch {branch!r} modifies forbidden path(s): {', '.join(bad)}",
                    "Fix:",
                    "  1) Revert the forbidden change(s) in the task branch",
                    "  2) Re-run the command",
                    f"Context: branch={git_current_branch(cwd=cwd)!r} cwd={Path.cwd().resolve()}",
                ]
            ),
            code=2,
        )

def task_title(task_id: str) -> str:
    tasks = load_tasks()
    tasks_by_id, _ = index_tasks_by_id(tasks)
    task = tasks_by_id.get(task_id)
    return str(task.get("title") or "").strip() if task else ""


def default_task_branch(task_id: str, slug: str) -> str:
    slug_norm = normalize_slug(slug)
    return f"task/{task_id}/{slug_norm}"


def cmd_branch_create(args: argparse.Namespace) -> None:
    require_not_task_worktree(action="branch create")
    ensure_git_clean(action="branch create")
    ensure_path_ignored(WORKTREES_DIRNAME, cwd=ROOT)

    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)

    if is_branch_pr_mode() and not args.agent:
        die("--agent is required in workflow_mode='branch_pr' (e.g., --agent CODER)", code=2)

    slug = normalize_slug(args.slug or task_title(task_id) or "work")
    base = (args.base or DEFAULT_MAIN_BRANCH).strip()
    branch = default_task_branch(task_id, slug)

    if not git_branch_exists(base):
        die(f"Base branch does not exist: {base}", code=2)

    expected_worktree_path = WORKTREES_DIR / f"{task_id}-{slug}"

    attached = detect_worktree_path_for_branch(branch, cwd=ROOT)
    if attached and attached != expected_worktree_path.resolve():
        die(f"Branch is already checked out in another worktree: {attached}", code=2)
    if attached and not args.reuse:
        die(f"Branch is already checked out in an existing worktree: {attached} (use --reuse)", code=2)

    if git_branch_exists(branch) and not args.reuse:
        die(f"Branch already exists: {branch} (use --reuse to reuse an existing worktree)", code=2)

    if args.worktree:
        WORKTREES_DIR.mkdir(parents=True, exist_ok=True)
        worktree_path = expected_worktree_path
        if worktree_path.exists():
            if not args.reuse:
                die(f"Worktree path already exists: {worktree_path} (use --reuse if it's a registered worktree)", code=2)
            registered_branch = detect_branch_for_worktree_path(worktree_path, cwd=ROOT)
            if registered_branch != branch:
                die(
                    f"Worktree path exists but is not registered for {branch!r}: {worktree_path}\n"
                    f"Registered: {registered_branch!r}",
                    code=2,
                )
            print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
            print_block("ACTION", f"Reuse existing worktree for {branch}")
            print_block("RESULT", f"branch={branch} worktree={worktree_path}")
            print_block("NEXT", "Open the worktree in your IDE and continue work there.")
            return
        try:
            if git_branch_exists(branch):
                run(["git", "worktree", "add", str(worktree_path), branch], check=True)
            else:
                run(["git", "worktree", "add", "-b", branch, str(worktree_path), base], check=True)
        except subprocess.CalledProcessError as exc:
            die(exc.stderr.strip() or exc.stdout.strip() or "git worktree add failed")
        if not args.quiet:
            print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
            print_block("ACTION", f"Create task branch + worktree for {task_id} (agent={args.agent or '-'})")
            print_block("RESULT", f"branch={branch} worktree={worktree_path}")
            print_block("NEXT", f"Open `{worktree_path}` in your IDE and run `python scripts/agentctl.py pr open {task_id} --branch {branch} --author {args.agent or 'CODER'}`.")
        return

    try:
        run(["git", "switch", "-c", branch, base], check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or exc.stdout.strip() or "git switch failed")
    if not args.quiet:
        print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
        print_block("ACTION", f"Create and switch to task branch for {task_id} (agent={args.agent or '-'})")
        print_block("RESULT", f"branch={branch}")
        print_block("NEXT", f"Run `python scripts/agentctl.py pr open {task_id} --branch {branch} --author {args.agent or 'CODER'}`.")


def _git_ahead_behind(branch: str, base: str, *, cwd: Path) -> Tuple[int, int]:
    try:
        result = run(["git", "rev-list", "--left-right", "--count", f"{base}...{branch}"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to compute ahead/behind")
    raw = (result.stdout or "").strip()
    if not raw:
        return 0, 0
    parts = raw.split()
    if len(parts) != 2:
        return 0, 0
    behind = int(parts[0])
    ahead = int(parts[1])
    return ahead, behind


def cmd_branch_status(args: argparse.Namespace) -> None:
    cwd = Path.cwd().resolve()
    branch = (args.branch or git_current_branch(cwd=cwd)).strip()
    base = (args.base or DEFAULT_MAIN_BRANCH).strip()
    if not git_branch_exists(branch, cwd=cwd):
        die(f"Unknown branch: {branch}", code=2)
    if not git_branch_exists(base, cwd=cwd):
        die(f"Unknown base branch: {base}", code=2)

    task_id = parse_task_id_from_task_branch(branch)
    worktree = detect_worktree_path_for_branch(branch, cwd=cwd)
    ahead, behind = _git_ahead_behind(branch, base, cwd=cwd)

    print_block("CONTEXT", format_command_context(cwd=cwd))
    print_block("RESULT", f"branch={branch} base={base} ahead={ahead} behind={behind} task_id={task_id or '-'}")
    if worktree:
        print_block("RESULT", f"worktree={worktree}")
    print_block("NEXT", "If you are ready, update PR artifacts via `python scripts/agentctl.py pr update <T-###>`.")


def cmd_branch_remove(args: argparse.Namespace) -> None:
    require_not_task_worktree(action="branch remove")

    branch = (args.branch or "").strip()
    worktree = (args.worktree or "").strip()
    if not branch and not worktree:
        die("Provide --branch and/or --worktree", code=2)

    if worktree:
        path = (ROOT / worktree).resolve() if not Path(worktree).is_absolute() else Path(worktree).resolve()
        worktrees_root = WORKTREES_DIR.resolve()
        if worktrees_root not in path.parents and path != worktrees_root:
            die(f"Refusing to remove worktree outside {worktrees_root}: {path}", code=2)
        try:
            cmd = ["git", "worktree", "remove"]
            if args.force:
                cmd.append("--force")
            cmd.append(str(path))
            run(cmd, check=True)
        except subprocess.CalledProcessError as exc:
            die(exc.stderr.strip() or exc.stdout.strip() or "git worktree remove failed")
        if not args.quiet:
            print(f"✅ removed worktree {path}")

    if branch:
        if not git_branch_exists(branch):
            die(f"Unknown branch: {branch}", code=2)
        try:
            run(["git", "branch", "-D" if args.force else "-d", branch], check=True)
        except subprocess.CalledProcessError as exc:
            die(exc.stderr.strip() or exc.stdout.strip() or "git branch delete failed")
        if not args.quiet:
            print(f"✅ removed branch {branch}")


def _run_agentctl_in_checkout(args: List[str], *, cwd: Path, quiet: bool) -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/agentctl.py", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        die(err or out or f"agentctl failed: {' '.join(args)}", code=proc.returncode or 2)
    if not quiet:
        out = (proc.stdout or "").strip()
        if out:
            print(out)


def cmd_work_start(args: argparse.Namespace) -> None:
    require_not_task_worktree(action="work start")
    ensure_git_clean(action="work start")
    ensure_path_ignored(WORKTREES_DIRNAME, cwd=ROOT)

    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)

    agent = (args.agent or "").strip()
    if is_branch_pr_mode() and not agent:
        die("--agent is required in workflow_mode='branch_pr' (e.g., --agent CODER)", code=2)

    if is_branch_pr_mode() and not getattr(args, "worktree", False):
        die("--worktree is required in workflow_mode='branch_pr' for `work start`", code=2)

    slug = normalize_slug(args.slug or task_title(task_id) or "work")
    base = (args.base or DEFAULT_MAIN_BRANCH).strip()
    branch = default_task_branch(task_id, slug)
    worktree_path = WORKTREES_DIR / f"{task_id}-{slug}"

    print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
    print_block("ACTION", f"Initialize task checkout for {task_id} (branch+PR+README)")

    cmd_branch_create(
        argparse.Namespace(
            task_id=task_id,
            agent=agent,
            slug=slug,
            base=base,
            worktree=bool(args.worktree),
            reuse=bool(args.reuse),
            quiet=True,
        )
    )

    if not worktree_path.exists():
        die(f"Expected worktree not found: {worktree_path}", code=2)

    readme_in_worktree = worktree_path / "docs" / "workflow" / task_id / "README.md"
    if readme_in_worktree.exists() and not getattr(args, "overwrite", False):
        pass
    else:
        scaffold_args = ["task", "scaffold", task_id, "--quiet"]
        if getattr(args, "overwrite", False):
            scaffold_args.insert(-1, "--overwrite")
        _run_agentctl_in_checkout(scaffold_args, cwd=worktree_path, quiet=True)

    pr_path = worktree_path / "docs" / "workflow" / task_id / "pr"
    if pr_path.exists():
        _run_agentctl_in_checkout(["pr", "update", task_id, "--quiet"], cwd=worktree_path, quiet=True)
        pr_action = "updated"
    else:
        _run_agentctl_in_checkout(
            ["pr", "open", task_id, "--branch", branch, "--base", base, "--author", agent, "--quiet"],
            cwd=worktree_path,
            quiet=True,
        )
        pr_action = "opened"

    if not args.quiet:
        print_block("RESULT", f"branch={branch} worktree={worktree_path} pr={pr_action}")
        print_block(
            "NEXT",
            "\n".join(
                [
                    f"Open `{worktree_path}` in your IDE",
                    f"Edit `docs/workflow/{task_id}/README.md` and implement changes",
                    f"Update PR artifacts: `python scripts/agentctl.py pr update {task_id}`",
                ]
            ),
        )


def git_list_task_branches(*, cwd: Path = ROOT) -> List[str]:
    try:
        result = run(["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/task"], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        die(exc.stderr.strip() or "Failed to list task branches")
    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def cmd_cleanup_merged(args: argparse.Namespace) -> None:
    require_not_task_worktree(action="cleanup merged")
    ensure_invoked_from_repo_root(action="cleanup merged")
    require_branch(DEFAULT_MAIN_BRANCH, action="cleanup merged")
    ensure_git_clean(action="cleanup merged")

    base = (args.base or DEFAULT_MAIN_BRANCH).strip()
    if not git_branch_exists(base):
        die(f"Unknown base branch: {base}", code=2)

    tasks = load_tasks()
    tasks_by_id, _ = index_tasks_by_id(tasks)

    candidates: List[Dict[str, str]] = []
    for branch in git_list_task_branches(cwd=ROOT):
        task_id = parse_task_id_from_task_branch(branch)
        if not task_id:
            continue
        task = tasks_by_id.get(task_id) or {}
        if str(task.get("status") or "").strip().upper() != "DONE":
            continue
        if git_diff_names(base, branch):
            continue
        worktree_path = detect_worktree_path_for_branch(branch, cwd=ROOT) or ""
        candidates.append({"task_id": task_id, "branch": branch, "worktree": worktree_path})

    print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
    print_block("ACTION", f"Cleanup merged task branches/worktrees (base={base})")

    if not candidates:
        print_block("RESULT", "no candidates")
        return

    lines = []
    for item in candidates:
        wt = item["worktree"] or "-"
        lines.append(f"- {item['task_id']}: branch={item['branch']} worktree={wt}")
    print_block("RESULT", "\n".join(lines))

    if not getattr(args, "yes", False):
        print_block("NEXT", "Re-run with `--yes` to delete these branches/worktrees.")
        return

    for item in candidates:
        wt = item["worktree"]
        cmd_branch_remove(
            argparse.Namespace(
                branch=item["branch"],
                worktree=wt or None,
                force=True,
                quiet=bool(args.quiet),
            )
        )
    if not args.quiet:
        print_block("RESULT", f"deleted={len(candidates)}")


def workflow_task_dir(task_id: str) -> Path:
    return WORKFLOW_DIR / task_id


def workflow_task_readme_path(task_id: str) -> Path:
    # Canonical per-task documentation (replaces docs/workflow/T-###.md and PR description.md).
    return workflow_task_dir(task_id) / "README.md"


def legacy_workflow_task_doc_path(task_id: str) -> Path:
    return WORKFLOW_DIR / f"{task_id}.md"


def pr_dir(task_id: str) -> Path:
    # New layout (T-074+): docs/workflow/T-###/pr/
    return workflow_task_dir(task_id) / "pr"


def legacy_pr_dir(task_id: str) -> Path:
    return PRS_DIR / task_id


def pr_dir_any(task_id: str) -> Path:
    new = pr_dir(task_id)
    if new.exists():
        return new
    old = legacy_pr_dir(task_id)
    if old.exists():
        return old
    return new


PR_DESCRIPTION_REQUIRED_SECTIONS: Tuple[str, ...] = (
    "Summary",
    "Scope",
    "Risks",
    "Verify Steps",
    "Rollback Plan",
)


def task_readme_template(task_id: str) -> str:
    title = task_title(task_id)
    header = f"# {task_id}: {title}" if title else f"# {task_id}"
    return "\n".join(
        [
            header,
            "",
            "## Summary",
            "",
            "- ...",
            "",
            "## Goal",
            "",
            "- ...",
            "",
            "## Scope",
            "",
            "- ...",
            "",
            "## Risks",
            "",
            "- ...",
            "",
            "## Verify Steps",
            "",
            "- ...",
            "",
            "## Rollback Plan",
            "",
            "- ...",
            "",
            "## Changes Summary (auto)",
            "",
            "<!-- BEGIN AUTO SUMMARY -->",
            "- (no file changes)",
            "<!-- END AUTO SUMMARY -->",
            "",
        ]
    )


def pr_review_template(task_id: str) -> str:
    return "\n".join(
        [
            f"# Review: {task_id}",
            "",
            "## Checklist",
            "",
            "- [ ] PR artifact complete (README/diffstat/verify.log)",
            "- [ ] No `tasks.json` changes in the task branch",
            "- [ ] Verify commands ran (or justified)",
            "- [ ] Scope matches task goal; risks understood",
            "",
            "## Handoff Notes",
            "",
            "Add short handoff notes here as list items so INTEGRATOR can append them to tasks.json on close.",
            "",
            "- CODER: ...",
            "- TESTER: ...",
            "- DOCS: ...",
            "- REVIEWER: ...",
            "",
            "## Notes",
            "",
            "- ...",
            "",
        ]
    )


def parse_handoff_notes(text: str) -> List[Dict[str, str]]:
    sections = extract_markdown_sections(text)
    lines = sections.get("Handoff Notes") or []
    notes: List[Dict[str, str]] = []
    for raw in lines:
        line = raw.strip()
        if not line.startswith("-"):
            continue
        payload = line.lstrip("-").strip()
        if not payload:
            continue
        if _is_placeholder_content(payload):
            continue
        if ":" not in payload:
            continue
        author, body = payload.split(":", 1)
        author = author.strip()
        body = body.strip()
        if not author or not body:
            continue
        if _is_placeholder_content(body):
            continue
        notes.append({"author": author, "body": body})
    return notes


def _is_placeholder_content(line: str) -> bool:
    stripped = (line or "").strip()
    if not stripped:
        return True
    lowered = stripped.lower()
    if lowered in {"...", "tbd", "todo", "- ...", "* ..."}:
        return True
    if re.fullmatch(r"[-*]\s*\.\.\.\s*", stripped):
        return True
    if re.fullmatch(r"\.+", stripped):
        return True
    return False


def extract_markdown_sections(text: str) -> Dict[str, List[str]]:
    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None
    for raw in (text or "").splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def pr_validate_description(text: str) -> Tuple[List[str], List[str]]:
    missing_sections: List[str] = []
    empty_sections: List[str] = []
    sections = extract_markdown_sections(text)
    for section in PR_DESCRIPTION_REQUIRED_SECTIONS:
        if section not in sections:
            missing_sections.append(section)
            continue
        lines = [ln for ln in sections.get(section, []) if ln.strip()]
        meaningful = [ln for ln in lines if not _is_placeholder_content(ln)]
        if not meaningful:
            empty_sections.append(section)
    return missing_sections, empty_sections


def pr_load_meta(meta_path: Path) -> Dict:
    if not meta_path.exists():
        return {}
    data = load_json(meta_path)
    return data if isinstance(data, dict) else {}


def pr_load_meta_text(text: str, *, source: str) -> Dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON in {source}: {exc}", code=2)
    return data if isinstance(data, dict) else {}


def pr_try_read_file_text(task_id: str, filename: str, *, branch: Optional[str]) -> Optional[str]:
    candidates = [pr_dir(task_id) / filename, legacy_pr_dir(task_id) / filename]
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
    if not branch:
        return None
    for path in candidates:
        rel = path.relative_to(ROOT).as_posix()
        text = git_show_text(branch, rel, cwd=ROOT)
        if text is not None:
            return text
    return None


def pr_try_read_doc_text(task_id: str, *, branch: Optional[str]) -> Optional[str]:
    """
    PR "description" doc:
      - New layout: docs/workflow/T-###/README.md
      - Legacy layout: docs/workflow/prs/T-###/description.md
    """
    readme = workflow_task_readme_path(task_id)
    if branch:
        rel = readme.relative_to(ROOT).as_posix()
        text = git_show_text(branch, rel, cwd=ROOT)
        if text is not None:
            return text
    if readme.exists():
        return readme.read_text(encoding="utf-8", errors="replace")
    legacy_description = legacy_pr_dir(task_id) / "description.md"
    if legacy_description.exists():
        return legacy_description.read_text(encoding="utf-8", errors="replace")
    if branch:
        rel = legacy_description.relative_to(ROOT).as_posix()
        return git_show_text(branch, rel, cwd=ROOT)
    return None


def pr_read_file_text(task_id: str, filename: str, *, branch: Optional[str]) -> str:
    text = pr_try_read_file_text(task_id, filename, branch=branch)
    if text is not None:
        return text
    target = pr_dir(task_id)
    legacy = legacy_pr_dir(task_id)
    if not branch:
        die(
            "\n".join(
                [
                    "Missing PR artifact dir in this checkout.",
                    "Fix:",
                    f"  1) Re-run with `--branch task/{task_id}/<slug>` so agentctl can read PR artifacts from that branch",
                    "  2) Or check out the task branch that contains the PR artifact files",
                    f"Expected (new): {target.relative_to(ROOT)}",
                    f"Fallback (legacy): {legacy.relative_to(ROOT)}",
                    f"Context: {format_command_context(cwd=Path.cwd().resolve())}",
                ]
            ),
            code=2,
        )

    rel = (target / filename).relative_to(ROOT).as_posix()
    legacy_rel = (legacy / filename).relative_to(ROOT).as_posix()
    die(
        "\n".join(
            [
                f"Missing PR artifact file in {branch!r}: {rel} (or legacy {legacy_rel})",
                "Fix:",
                f"  1) Ensure the task branch contains `{rel}` (run `python scripts/agentctl.py pr open {task_id}` in the branch)",
                "  2) Commit the PR artifact files to the task branch",
                "  3) Re-run the command",
                f"Context: {format_command_context(cwd=Path.cwd().resolve())}",
            ]
        ),
        code=2,
    )


def pr_write_meta(meta_path: Path, meta: Dict) -> None:
    write_json(meta_path, meta)


def pr_ensure_skeleton(*, task_id: str, branch: str, author: str, base_branch: str) -> Path:
    target = pr_dir(task_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=True, exist_ok=True)

    readme_path = workflow_task_readme_path(task_id)
    if not readme_path.exists():
        readme_path.write_text(task_readme_template(task_id), encoding="utf-8")

    meta_path = target / "meta.json"
    meta = pr_load_meta(meta_path)
    created_at = meta.get("created_at") if isinstance(meta.get("created_at"), str) else now_iso_utc()

    meta.update(
        {
            "task_id": task_id,
            "task_title": task_title(task_id),
            "branch": branch,
            "base_branch": base_branch,
            "author": author,
            "created_at": created_at,
            "updated_at": now_iso_utc(),
            "head_sha": git_rev_parse(branch),
            "merge_strategy": meta.get("merge_strategy") or "squash",
            "status": meta.get("status") or "OPEN",
        }
    )
    pr_write_meta(meta_path, meta)

    diffstat_path = target / "diffstat.txt"
    if not diffstat_path.exists():
        diffstat_path.write_text("", encoding="utf-8")

    verify_path = target / "verify.log"
    if not verify_path.exists():
        verify_path.write_text("# Verify log\n\n", encoding="utf-8")

    review_path = target / "review.md"
    if not review_path.exists():
        review_path.write_text(pr_review_template(task_id), encoding="utf-8")

    return target


def cmd_pr_open(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)
    author = (args.author or "").strip()
    if is_branch_pr_mode() and not author:
        die("--author is required in workflow_mode='branch_pr' (e.g., --author CODER)", code=2)
    if not author:
        author = "unknown"

    branch = (args.branch or git_current_branch()).strip()
    base = (args.base or DEFAULT_MAIN_BRANCH).strip()
    if branch == base:
        die(f"Refusing to open PR on base branch {base!r}", code=2)
    if not git_branch_exists(branch):
        die(f"Unknown branch: {branch}", code=2)

    target = pr_dir(task_id)
    legacy_target = legacy_pr_dir(task_id)
    if target.exists() or legacy_target.exists():
        existing = target if target.exists() else legacy_target
        die(f"PR artifact dir already exists: {existing} (use `pr update`)", code=2)

    target = pr_ensure_skeleton(task_id=task_id, branch=branch, author=author, base_branch=base)
    cmd_pr_update(argparse.Namespace(task_id=task_id, branch=branch, base=base, quiet=True))
    if not args.quiet:
        print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
        print_block("ACTION", f"Open PR artifact for {task_id}")
        print_block("RESULT", f"dir={target.relative_to(ROOT)} branch={branch} base={base} author={author}")
        readme_rel = workflow_task_readme_path(task_id).relative_to(ROOT)
        print_block("NEXT", f"Fill out `{readme_rel}` then run `python scripts/agentctl.py pr check {task_id}`.")


def update_task_readme_auto_summary(task_id: str, *, changed: List[str]) -> None:
    readme_path = workflow_task_readme_path(task_id)
    if not readme_path.exists():
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        readme_path.write_text(task_readme_template(task_id), encoding="utf-8")
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    begin_marker = "<!-- BEGIN AUTO SUMMARY -->"
    end_marker = "<!-- END AUTO SUMMARY -->"
    begins = [i for i, line in enumerate(lines) if line.strip() == begin_marker]
    if not begins:
        return
    begin = max(begins)
    ends_after = [i for i, line in enumerate(lines) if i > begin and line.strip() == end_marker]
    if not ends_after:
        return
    end = min(ends_after)
    summary_lines = [f"- `{name}`" for name in (changed or [])[:20]]
    if not summary_lines:
        summary_lines = ["- (no file changes)"]
    new_lines = lines[: begin + 1] + summary_lines + lines[end:]
    new_text = "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")
    if new_text != text:
        readme_path.write_text(new_text, encoding="utf-8")


def cmd_pr_update(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)

    target = pr_dir_any(task_id)
    if not target.exists():
        die(f"Missing PR artifact dir: {target}", code=2)

    meta_path = target / "meta.json"
    meta = pr_load_meta(meta_path)
    branch = (args.branch or str(meta.get("branch") or "")).strip() or git_current_branch()
    base = (args.base or str(meta.get("base_branch") or DEFAULT_MAIN_BRANCH)).strip()
    if not git_branch_exists(branch):
        die(f"Unknown branch: {branch}", code=2)

    diffstat = git_diff_stat(base, branch)
    (target / "diffstat.txt").write_text(diffstat, encoding="utf-8")

    meta.update(
        {
            "updated_at": now_iso_utc(),
            "head_sha": git_rev_parse(branch),
            "branch": branch,
            "base_branch": base,
        }
    )
    pr_write_meta(meta_path, meta)

    update_task_readme_auto_summary(task_id, changed=git_diff_names(base, branch))

    if not args.quiet:
        print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
        print_block("ACTION", f"Update PR artifact for {task_id}")
        print_block("RESULT", f"dir={target.relative_to(ROOT)} branch={branch} base={base}")
        print_block("NEXT", f"Run `python scripts/agentctl.py pr check {task_id} --branch {branch} --base {base}`.")


def pr_check(
    task_id: str,
    *,
    branch: Optional[str] = None,
    base: Optional[str] = None,
    quiet: bool = False,
) -> None:
    target = pr_dir(task_id)
    meta_rel = (target / "meta.json").relative_to(ROOT).as_posix()
    meta_text = pr_read_file_text(task_id, "meta.json", branch=branch)
    meta_source = meta_rel if (target / "meta.json").exists() else f"{branch}:{meta_rel}"
    meta = pr_load_meta_text(meta_text, source=meta_source)
    meta_task_id = str(meta.get("task_id") or "").strip()
    if meta_task_id and meta_task_id != task_id:
        die(f"PR meta.json task_id mismatch: expected {task_id}, got {meta_task_id}", code=2)

    base_branch = (base or str(meta.get("base_branch") or DEFAULT_MAIN_BRANCH)).strip()
    meta_branch = str(meta.get("branch") or "").strip()
    if branch and meta_branch and meta_branch != branch:
        die(f"PR meta.json branch mismatch: expected {branch}, got {meta_branch}", code=2)
    pr_branch = (branch or meta_branch) or git_current_branch()
    if git_status_porcelain(cwd=Path.cwd().resolve()):
        die(f"Working tree is dirty (pr check requires clean state)\nContext: {format_command_context(cwd=Path.cwd().resolve())}", code=2)
    if not git_branch_exists(pr_branch):
        die(f"Unknown branch: {pr_branch}", code=2)
    if not git_branch_exists(base_branch):
        die(f"Unknown base branch: {base_branch}", code=2)
    parsed_task_id = parse_task_id_from_task_branch(pr_branch)
    if is_branch_pr_mode() and parsed_task_id != task_id:
        die(f"Branch {pr_branch!r} does not match task id {task_id} (expected task/{task_id}/<slug>)", code=2)

    required_files = ["meta.json", "diffstat.txt", "verify.log"]
    artifact_branch = pr_branch if not target.exists() else None
    missing_files = [name for name in required_files if pr_try_read_file_text(task_id, name, branch=artifact_branch) is None]
    if missing_files:
        die(f"Missing PR artifact file(s): {', '.join(missing_files)}", code=2)

    pr_doc = pr_try_read_doc_text(task_id, branch=artifact_branch)
    if pr_doc is None:
        readme_rel = workflow_task_readme_path(task_id).relative_to(ROOT).as_posix()
        legacy_rel = (legacy_pr_dir(task_id) / "description.md").relative_to(ROOT).as_posix()
        die(f"Missing PR doc: {readme_rel} (or legacy {legacy_rel})", code=2)
    missing_sections, empty_sections = pr_validate_description(pr_doc)
    doc_hint = workflow_task_readme_path(task_id).relative_to(ROOT).as_posix()
    if missing_sections:
        die(f"PR doc {doc_hint} missing required section(s): {', '.join(missing_sections)}", code=2)
    if empty_sections:
        die(f"PR doc {doc_hint} has empty section(s): {', '.join(empty_sections)}", code=2)

    subjects = git_log_subjects(base_branch, pr_branch, limit=200)
    if not subjects:
        die(f"No commits found on {pr_branch!r} compared to {base_branch!r}", code=2)
    if not any(task_id in subject for subject in subjects):
        die(f"Branch {pr_branch!r} has no commit subject mentioning {task_id}", code=2)

    changed = git_diff_names(base_branch, pr_branch)
    if "tasks.json" in changed:
        die(f"Branch {pr_branch!r} modifies tasks.json (single-writer violation)", code=2)

    if not quiet:
        print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
        print_block("ACTION", f"Validate PR for {task_id}")
        print_block("RESULT", f"dir={target.relative_to(ROOT)} branch={pr_branch} base={base_branch}")
        print_block("NEXT", "If green, INTEGRATOR can run `python scripts/agentctl.py integrate ...`.")


def cmd_pr_check(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)
    pr_check(task_id, branch=args.branch, base=args.base, quiet=bool(args.quiet))


def append_pr_handoff_note(review_path: Path, *, author: str, body: str) -> None:
    author_clean = (author or "").strip()
    body_clean = (body or "").strip()
    if not author_clean:
        die("--author must be non-empty", code=2)
    if not body_clean:
        die("--body must be non-empty", code=2)

    note_line = f"- {author_clean}: {body_clean}"
    text = review_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    header = "## Handoff Notes"
    try:
        header_idx = next(i for i, line in enumerate(lines) if line.strip() == header)
    except StopIteration:
        die(f"Missing section {header!r} in {review_path.relative_to(ROOT)}", code=2)

    next_header_idx = None
    for idx in range(header_idx + 1, len(lines)):
        if lines[idx].strip().startswith("## "):
            next_header_idx = idx
            break
    section_end = next_header_idx if next_header_idx is not None else len(lines)

    if note_line in [ln.rstrip() for ln in lines[header_idx + 1 : section_end]]:
        return

    insert_at = section_end
    while insert_at > header_idx + 1 and not lines[insert_at - 1].strip():
        insert_at -= 1

    new_lines = list(lines)
    new_lines.insert(insert_at, note_line)
    review_path.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


def cmd_pr_note(args: argparse.Namespace) -> None:
    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)
    author = (args.author or "").strip()
    body = (args.body or "").strip()
    if not author:
        die("--author is required (e.g., --author CODER)", code=2)
    if not body:
        die("--body is required", code=2)

    target = pr_dir_any(task_id)
    review_path = target / "review.md"
    if not review_path.exists():
        die(
            "\n".join(
                [
                    f"Missing PR artifact file: {review_path.relative_to(ROOT)}",
                    "Fix:",
                    f"  1) Run `python scripts/agentctl.py pr open {task_id} --author {author} --branch task/{task_id}/<slug>`",
                    "  2) Commit the PR artifact files on the task branch",
                    f"  3) Re-run `python scripts/agentctl.py pr note {task_id} --author {author} --body \"...\"`",
                    f"Context: {format_command_context(cwd=Path.cwd().resolve())}",
                ]
            ),
            code=2,
        )

    append_pr_handoff_note(review_path, author=author, body=body)
    if not args.quiet:
        print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
        print_block("ACTION", f"Append handoff note for {task_id}")
        print_block("RESULT", f"path={review_path.relative_to(ROOT)} author={author}")


def get_task_verify_commands_for(task_id: str) -> List[str]:
    data = load_json(TASKS_PATH)
    task = _ensure_task_object(data, task_id)
    verify = task.get("verify")
    if verify is None:
        return []
    if isinstance(verify, list):
        return [cmd.strip() for cmd in verify if isinstance(cmd, str) and cmd.strip()]
    die(f"{task_id}: verify must be a list of strings", code=2)
    return []


def append_verify_log(path: Path, *, header: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(header.rstrip() + "\n")
        if content:
            handle.write(content.rstrip() + "\n")
        handle.write("\n")


def run_verify_with_capture(
    task_id: str,
    *,
    cwd: Path,
    quiet: bool,
    log_path: Optional[Path] = None,
    current_sha: Optional[str] = None,
) -> List[Tuple[str, str]]:
    commands = get_task_verify_commands_for(task_id)
    entries: List[Tuple[str, str]] = []
    if not commands:
        timestamp = now_iso_utc()
        header = f"[{timestamp}] ℹ️ no verify commands configured"
        entries.append((header, ""))
        if log_path:
            append_verify_log(log_path, header=header, content="")
        if not quiet:
            print(f"ℹ️ {task_id}: no verify commands configured")
        return entries

    for command in commands:
        if not quiet:
            print(f"$ {command}")
        timestamp = now_iso_utc()
        proc = subprocess.run(command, cwd=str(cwd), shell=True, text=True, capture_output=True)
        output = ""
        if proc.stdout:
            output += proc.stdout
        if proc.stderr:
            output += ("\n" if output and not output.endswith("\n") else "") + proc.stderr
        sha_prefix = f"sha={current_sha} " if current_sha else ""
        header = f"[{timestamp}] {sha_prefix}$ {command}".rstrip()
        entries.append((header, output))
        if log_path:
            append_verify_log(log_path, header=header, content=output)
        if proc.returncode != 0:
            raise SystemExit(proc.returncode)
    if current_sha:
        timestamp = now_iso_utc()
        header = f"[{timestamp}] ✅ verified_sha={current_sha}"
        entries.append((header, ""))
        if log_path:
            append_verify_log(log_path, header=header, content="")
    if not quiet:
        print(f"✅ verify passed for {task_id}")
    return entries


def cmd_integrate(args: argparse.Namespace) -> None:
    require_not_task_worktree(action="integrate")
    ensure_invoked_from_repo_root(action="integrate")
    require_branch(DEFAULT_MAIN_BRANCH, action="integrate")
    ensure_git_clean(action="integrate")
    ensure_path_ignored(WORKTREES_DIRNAME, cwd=ROOT)

    task_id = args.task_id.strip()
    if not task_id:
        die("task_id must be non-empty", code=2)

    pr_path = pr_dir(task_id)
    branch = (args.branch or "").strip()
    if not branch:
        existing_meta = pr_load_meta(pr_path / "meta.json")
        branch = str(existing_meta.get("branch") or "").strip()
    if not branch:
        die("Missing --branch (and PR meta.json is not available in this checkout)", code=2)

    meta_rel = (pr_path / "meta.json").relative_to(ROOT).as_posix()
    meta_text = pr_read_file_text(task_id, "meta.json", branch=branch)
    meta_source = meta_rel if (pr_path / "meta.json").exists() else f"{branch}:{meta_rel}"
    meta = pr_load_meta_text(meta_text, source=meta_source)

    base = (args.base or str(meta.get("base_branch") or DEFAULT_MAIN_BRANCH)).strip()
    strategy = (args.merge_strategy or str(meta.get("merge_strategy") or "squash")).strip().lower()
    if strategy not in {"squash", "merge", "rebase"}:
        die("--merge-strategy must be squash|merge|rebase", code=2)

    print_block("CONTEXT", format_command_context(cwd=Path.cwd().resolve()))
    print_block("ACTION", f"Integrate {branch} into {base} for {task_id} (strategy={strategy})")

    pr_check(task_id, branch=branch, base=base, quiet=True)
    assert_no_diff_paths(base=base, branch=branch, forbidden=["tasks.json"], cwd=ROOT)
    base_sha_before_merge = git_rev_parse(base)

    verify_commands = get_task_verify_commands_for(task_id)
    branch_head_sha = git_rev_parse(branch)
    already_verified_sha: Optional[str] = None
    if verify_commands and not args.run_verify:
        meta_verified = str(meta.get("last_verified_sha") or "").strip()
        if meta_verified and meta_verified == branch_head_sha:
            already_verified_sha = branch_head_sha
        else:
            log_text = pr_try_read_file_text(task_id, "verify.log", branch=branch)
            if log_text:
                log_verified = extract_last_verified_sha_from_log(log_text)
                if log_verified and log_verified == branch_head_sha:
                    already_verified_sha = branch_head_sha
    should_run_verify = bool(args.run_verify) or (bool(verify_commands) and not already_verified_sha)

    worktree_path = detect_worktree_path_for_branch(branch, cwd=ROOT)
    created_temp = False
    temp_path = WORKTREES_DIR / f"_integrate_tmp_{task_id}"
    if strategy == "rebase" and not worktree_path:
        die("Rebase strategy requires an existing worktree for the task branch", code=2)
    if should_run_verify and not worktree_path:
        if args.dry_run:
            print_block("RESULT", f"verify_worktree=(would create {temp_path})")
        else:
            if temp_path.exists():
                registered = detect_branch_for_worktree_path(temp_path, cwd=ROOT)
                if not registered:
                    die(f"Temp worktree path exists but is not registered: {temp_path}", code=2)
            else:
                WORKTREES_DIR.mkdir(parents=True, exist_ok=True)
                try:
                    run(["git", "worktree", "add", str(temp_path), branch], check=True)
                except subprocess.CalledProcessError as exc:
                    die(exc.stderr.strip() or exc.stdout.strip() or "git worktree add failed")
                created_temp = True
            worktree_path = temp_path

    if args.dry_run:
        verify_label = "yes" if should_run_verify else "no"
        if verify_commands and not should_run_verify and already_verified_sha:
            verify_label = f"no (already verified_sha={already_verified_sha})"
        print_block("RESULT", f"pr_check=OK base={base} branch={branch} verify={verify_label}")
        print_block("NEXT", "Re-run without --dry-run to perform merge+finish.")
        return

    try:
        verify_entries: List[Tuple[str, str]] = []

        merge_hash = ""
        if strategy == "squash":
            if should_run_verify:
                if not worktree_path:
                    die("Unable to locate/create a worktree for verify execution", code=2)
                verify_entries = run_verify_with_capture(
                    task_id,
                    cwd=worktree_path,
                    quiet=bool(args.quiet),
                    log_path=None,
                    current_sha=branch_head_sha,
                )
            run(["git", "merge", "--squash", branch], check=True)
            subject = run(["git", "log", "-1", "--pretty=format:%s", branch], cwd=ROOT, check=True).stdout.strip()
            if not subject or task_id not in subject:
                subject = f"🧩 {task_id} integrate {branch}"
            run(["git", "commit", "-m", subject], check=True)
            merge_hash = git_rev_parse("HEAD")
        elif strategy == "merge":
            if should_run_verify:
                if not worktree_path:
                    die("Unable to locate/create a worktree for verify execution", code=2)
                verify_entries = run_verify_with_capture(
                    task_id,
                    cwd=worktree_path,
                    quiet=bool(args.quiet),
                    log_path=None,
                    current_sha=branch_head_sha,
                )
            run(["git", "merge", "--no-ff", branch, "-m", f"🔀 {task_id} merge {branch}"], check=True)
            merge_hash = git_rev_parse("HEAD")
        else:
            proc = run(["git", "rebase", base], cwd=worktree_path, check=False)
            if proc.returncode != 0:
                run(["git", "rebase", "--abort"], cwd=worktree_path, check=False)
                die(proc.stderr.strip() or proc.stdout.strip() or "git rebase failed", code=2)
            branch_head_sha = git_rev_parse(branch)
            if verify_commands and not args.run_verify:
                already_verified_sha = None
                meta_verified = str(meta.get("last_verified_sha") or "").strip()
                if meta_verified and meta_verified == branch_head_sha:
                    already_verified_sha = branch_head_sha
                else:
                    log_text = pr_try_read_file_text(task_id, "verify.log", branch=branch)
                    if log_text:
                        log_verified = extract_last_verified_sha_from_log(log_text)
                        if log_verified and log_verified == branch_head_sha:
                            already_verified_sha = branch_head_sha
                should_run_verify = bool(verify_commands) and not already_verified_sha
            if should_run_verify:
                verify_entries = run_verify_with_capture(
                    task_id,
                    cwd=worktree_path,
                    quiet=bool(args.quiet),
                    log_path=None,
                    current_sha=branch_head_sha,
                )
            run(["git", "merge", "--ff-only", branch], check=True)
            merge_hash = git_rev_parse("HEAD")

        if not verify_commands:
            verify_desc = "skipped(no commands)"
        elif should_run_verify:
            verify_desc = "ran"
        elif already_verified_sha:
            verify_desc = f"skipped(already verified_sha={already_verified_sha})"
        else:
            verify_desc = "skipped"
        finish_body = f"Verified: Integrated via {strategy}; verify={verify_desc}; pr={pr_path.relative_to(ROOT)}."
        cmd_finish(
            argparse.Namespace(
                task_id=task_id,
                commit=merge_hash,
                author="INTEGRATOR",
                body=finish_body,
                skip_verify=True,
                quiet=bool(args.quiet),
                force=False,
                require_task_id_in_commit=True,
            )
        )
        cmd_task_lint(argparse.Namespace(quiet=bool(args.quiet)))

        if not pr_path.exists():
            die(f"Missing PR artifact dir after merge: {pr_path}", code=2)
        if should_run_verify and verify_entries:
            verify_log = pr_path / "verify.log"
            for header, content in verify_entries:
                append_verify_log(verify_log, header=header, content=content)
        meta_path = pr_path / "meta.json"
        meta_main = pr_load_meta(meta_path)
        now = now_iso_utc()
        meta_main.update(
            {
                "merge_strategy": strategy,
                "status": "MERGED",
                "merged_at": meta_main.get("merged_at") or now,
                "merge_commit": merge_hash,
                "head_sha": branch_head_sha,
                "updated_at": now,
            }
        )
        if should_run_verify and verify_entries:
            if branch_head_sha:
                meta_main["last_verified_sha"] = branch_head_sha
                meta_main["last_verified_at"] = now
        pr_write_meta(meta_path, meta_main)

        (pr_path / "diffstat.txt").write_text(git_diff_stat(base_sha_before_merge, branch), encoding="utf-8")
        update_task_readme_auto_summary(task_id, changed=git_diff_names(base_sha_before_merge, branch))

        print_block("RESULT", f"merge_commit={merge_hash} finish=OK")
        print_block(
            "NEXT",
            f"Commit closure on main: stage `tasks.json` + `{(pr_path / 'meta.json').relative_to(ROOT)}` (and any docs), then commit `✅ {task_id} close ...`.",
        )
    finally:
        if created_temp:
            run(["git", "worktree", "remove", "--force", str(temp_path)], check=False)


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
    p_verify.add_argument("--cwd", help="Run verify commands in this repo subdirectory/worktree (must be under repo root)")
    p_verify.add_argument("--log", help="Append output to a log file (e.g., docs/workflow/T-123/pr/verify.log)")
    p_verify.add_argument(
        "--skip-if-unchanged",
        action="store_true",
        help="Skip verify when the current SHA matches the last verified SHA (when available via PR meta/log).",
    )
    p_verify.add_argument("--quiet", action="store_true", help="Minimal output")
    p_verify.add_argument("--require", action="store_true", help="Fail if no verify commands exist")
    p_verify.set_defaults(func=cmd_verify)

    p_work = sub.add_parser("work", help="One-command helpers to start a task checkout")
    work_sub = p_work.add_subparsers(dest="work_cmd", required=True)

    p_work_start = work_sub.add_parser("start", help="Create branch+worktree and initialize per-task artifacts")
    p_work_start.add_argument("task_id")
    p_work_start.add_argument("--agent", help="Agent creating the checkout (e.g., CODER)")
    p_work_start.add_argument("--slug", required=True, help="Short slug for the branch/worktree name (e.g., work-start)")
    p_work_start.add_argument("--base", default=DEFAULT_MAIN_BRANCH, help=f"Base branch (default: {DEFAULT_MAIN_BRANCH})")
    p_work_start.add_argument("--worktree", action="store_true", help=f"Create a worktree under {WORKTREES_DIRNAME}/")
    p_work_start.add_argument("--reuse", action="store_true", help="Reuse an existing registered worktree if present")
    p_work_start.add_argument("--overwrite", action="store_true", help="Overwrite docs/workflow/T-###/README.md when scaffolding")
    p_work_start.add_argument("--quiet", action="store_true", help="Minimal output")
    p_work_start.set_defaults(func=cmd_work_start)

    p_cleanup = sub.add_parser("cleanup", help="Cleanup helpers (dry-run by default)")
    cleanup_sub = p_cleanup.add_subparsers(dest="cleanup_cmd", required=True)

    p_cleanup_merged = cleanup_sub.add_parser("merged", help="Remove merged task branches and their worktrees")
    p_cleanup_merged.add_argument("--base", default=DEFAULT_MAIN_BRANCH, help=f"Base branch (default: {DEFAULT_MAIN_BRANCH})")
    p_cleanup_merged.add_argument("--yes", action="store_true", help="Actually delete; without this flag, prints a dry-run plan")
    p_cleanup_merged.add_argument("--quiet", action="store_true", help="Minimal output")
    p_cleanup_merged.set_defaults(func=cmd_cleanup_merged)

    p_branch = sub.add_parser("branch", help="Task branch + worktree helpers (single task per branch)")
    branch_sub = p_branch.add_subparsers(dest="branch_cmd", required=True)

    p_branch_create = branch_sub.add_parser("create", help="Create task branch (optionally with a git worktree)")
    p_branch_create.add_argument("task_id")
    p_branch_create.add_argument("--agent", help="Agent creating the branch (e.g., CODER)")
    p_branch_create.add_argument("--slug", required=True, help="Short slug for the branch/worktree name (e.g., auth-cache)")
    p_branch_create.add_argument("--base", default=DEFAULT_MAIN_BRANCH, help=f"Base branch (default: {DEFAULT_MAIN_BRANCH})")
    p_branch_create.add_argument("--worktree", action="store_true", help=f"Create a worktree under {WORKTREES_DIRNAME}/")
    p_branch_create.add_argument("--reuse", action="store_true", help="Reuse an existing registered worktree if present")
    p_branch_create.add_argument("--quiet", action="store_true", help="Minimal output")
    p_branch_create.set_defaults(func=cmd_branch_create)

    p_branch_status = branch_sub.add_parser("status", help="Show quick branch/task status (ahead/behind, worktree path)")
    p_branch_status.add_argument("--branch", help="Branch name (default: current branch)")
    p_branch_status.add_argument("--base", default=DEFAULT_MAIN_BRANCH, help=f"Base branch (default: {DEFAULT_MAIN_BRANCH})")
    p_branch_status.set_defaults(func=cmd_branch_status)

    p_branch_remove = branch_sub.add_parser("remove", help="Remove a task worktree and/or branch (manual confirmation recommended)")
    p_branch_remove.add_argument("--branch", help="Branch name to delete")
    p_branch_remove.add_argument("--worktree", help="Worktree path to remove (relative or absolute)")
    p_branch_remove.add_argument("--force", action="store_true", help="Force deletion")
    p_branch_remove.add_argument("--quiet", action="store_true", help="Minimal output")
    p_branch_remove.set_defaults(func=cmd_branch_remove)

    p_pr = sub.add_parser("pr", help="Local PR artifact helpers (docs/workflow/T-###/pr)")
    pr_sub = p_pr.add_subparsers(dest="pr_cmd", required=True)

    p_pr_open = pr_sub.add_parser("open", help="Create PR artifact folder + templates")
    p_pr_open.add_argument("task_id")
    p_pr_open.add_argument("--branch", help="Task branch name (default: current branch)")
    p_pr_open.add_argument("--base", default=DEFAULT_MAIN_BRANCH, help=f"Base branch (default: {DEFAULT_MAIN_BRANCH})")
    p_pr_open.add_argument("--author", help="Agent/author creating the PR artifact (e.g., CODER)")
    p_pr_open.add_argument("--quiet", action="store_true", help="Minimal output")
    p_pr_open.set_defaults(func=cmd_pr_open)

    p_pr_update = pr_sub.add_parser("update", help="Refresh PR meta + diffstat from git")
    p_pr_update.add_argument("task_id")
    p_pr_update.add_argument("--branch", help="Override branch name (default: from meta.json)")
    p_pr_update.add_argument("--base", help="Override base branch (default: from meta.json)")
    p_pr_update.add_argument("--quiet", action="store_true", help="Minimal output")
    p_pr_update.set_defaults(func=cmd_pr_update)

    p_pr_check = pr_sub.add_parser("check", help="Validate PR artifact completeness + branch invariants")
    p_pr_check.add_argument("task_id")
    p_pr_check.add_argument("--branch", help="Override branch name (default: from meta.json)")
    p_pr_check.add_argument("--base", help="Override base branch (default: from meta.json)")
    p_pr_check.add_argument("--quiet", action="store_true", help="Minimal output")
    p_pr_check.set_defaults(func=cmd_pr_check)

    p_pr_note = pr_sub.add_parser("note", help="Append a handoff note bullet to docs/workflow/T-###/pr/review.md")
    p_pr_note.add_argument("task_id")
    p_pr_note.add_argument("--author", required=True, help="Note author/role (e.g., CODER)")
    p_pr_note.add_argument("--body", required=True, help="Note body text")
    p_pr_note.add_argument("--quiet", action="store_true", help="Minimal output")
    p_pr_note.set_defaults(func=cmd_pr_note)

    p_integrate = sub.add_parser("integrate", help="Merge a task branch into main (gated by PR artifact + verify)")
    p_integrate.add_argument("task_id")
    p_integrate.add_argument("--branch", help="Task branch to integrate (default: from PR meta.json)")
    p_integrate.add_argument("--base", default=DEFAULT_MAIN_BRANCH, help=f"Base branch (default: {DEFAULT_MAIN_BRANCH})")
    p_integrate.add_argument("--merge-strategy", dest="merge_strategy", default="squash", help="squash|merge|rebase (default: squash)")
    p_integrate.add_argument("--run-verify", action="store_true", help="Run task verify commands (or always when configured) and append output to PR verify.log")
    p_integrate.add_argument("--dry-run", action="store_true", help="Print plan + preflight checks without making changes")
    p_integrate.add_argument("--quiet", action="store_true", help="Minimal output")
    p_integrate.set_defaults(func=cmd_integrate)

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
    p_guard_commit.add_argument(
        "--auto-allow",
        action="store_true",
        help="Derive --allow prefixes from staged files (useful when you don't know the minimal allowlist yet)",
    )
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

    p_scaffold = task_sub.add_parser("scaffold", help="Create docs/workflow/T-###/README.md skeleton for a task")
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
