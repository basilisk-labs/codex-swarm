from __future__ import annotations

import difflib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from urllib import error as urlerror
from urllib import parse as urlparse
from urllib import request as urlrequest


class RedmineUnavailable(RuntimeError):
    pass


def _load_local_backend_class() -> type:
    local_path = Path(__file__).resolve().parents[1] / "local" / "backend.py"
    spec = importlib.util.spec_from_file_location("local_backend", local_path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Unable to load local backend from {local_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    backend_cls = getattr(module, "LocalBackend", None)
    if backend_cls is None:
        raise RuntimeError("LocalBackend class not found")
    return backend_cls


class RedmineBackend:
    def __init__(self, settings: Optional[Dict[str, object]] = None) -> None:
        settings = settings if isinstance(settings, dict) else {}
        env_url = os.environ.get("CODEXSWARM_REDMINE_URL", "").strip()
        env_api_key = os.environ.get("CODEXSWARM_REDMINE_API_KEY", "").strip()
        env_project_id = os.environ.get("CODEXSWARM_REDMINE_PROJECT_ID", "").strip()
        env_assignee = os.environ.get("CODEXSWARM_REDMINE_ASSIGNEE_ID", "").strip()

        self.base_url = (env_url or str(settings.get("url") or "")).rstrip("/")
        self.api_key = env_api_key or str(settings.get("api_key") or "").strip()
        self.project_id = env_project_id or str(settings.get("project_id") or "").strip()
        self.assignee_id = int(env_assignee) if env_assignee.isdigit() else None
        self.status_map = settings.get("status_map") or {}
        self.custom_fields = settings.get("custom_fields") or {}
        cache_dir = str(settings.get("cache_dir") or ".codex-swarm/tasks")

        if not self.base_url or not self.api_key or not self.project_id:
            raise ValueError("Redmine backend requires url, api_key, and project_id")

        local_backend_cls = _load_local_backend_class()
        self.cache = local_backend_cls({"dir": cache_dir})

        self._reverse_status_map: Dict[int, str] = {}
        if isinstance(self.status_map, dict):
            for key, value in self.status_map.items():
                if isinstance(value, int):
                    self._reverse_status_map[value] = str(key)

    def generate_task_id(self, *, length: int = 6, attempts: int = 1000) -> str:
        existing_ids: set[str] = set()
        try:
            existing_ids = {
                str(task.get("id") or "")
                for task in self._list_tasks_remote()
                if isinstance(task, dict)
            }
        except RedmineUnavailable:
            existing_ids = {
                str(task.get("id") or "")
                for task in self.cache.list_tasks()
                if isinstance(task, dict)
            }
        for _ in range(attempts):
            candidate = self.cache.generate_task_id(length=length, attempts=1)
            if candidate not in existing_ids:
                return candidate
        raise RuntimeError("Failed to generate a unique task id")

    def list_tasks(self) -> List[Dict[str, object]]:
        try:
            tasks = self._list_tasks_remote()
        except RedmineUnavailable:
            return self.cache.list_tasks()
        for task in tasks:
            self._cache_task(task, dirty=False)
        return tasks

    def get_task(self, task_id: str) -> Optional[Dict[str, object]]:
        try:
            issue = self._find_issue_by_task_id(task_id)
            if issue is None:
                return None
            task = self._issue_to_task(issue)
            if task:
                self._cache_task(task, dirty=False)
            return task
        except RedmineUnavailable:
            return self.cache.get_task(task_id)

    def write_task(self, task: Dict[str, object]) -> None:
        task_id = str(task.get("id") or "").strip()
        if not task_id:
            raise ValueError("task.id is required")
        try:
            issue_id = task.get("redmine_id")
            if not issue_id:
                issue = self._find_issue_by_task_id(task_id)
                issue_id = issue.get("id") if isinstance(issue, dict) else None
            payload = self._task_to_issue_payload(task)
            if issue_id:
                self._request_json("PUT", f"issues/{issue_id}.json", payload={"issue": payload})
            else:
                payload["project_id"] = self.project_id
                created = self._request_json("POST", "issues.json", payload={"issue": payload})
                issue_id = (created.get("issue") or {}).get("id") if isinstance(created, dict) else None
                if issue_id:
                    update_payload = dict(payload)
                    update_payload.pop("project_id", None)
                    self._request_json("PUT", f"issues/{issue_id}.json", payload={"issue": update_payload})
            if issue_id:
                task["redmine_id"] = issue_id
            task["dirty"] = False
            self._cache_task(task, dirty=False)
        except RedmineUnavailable:
            task["dirty"] = True
            self._cache_task(task, dirty=True)

    def sync(self, direction: str = "push", conflict: str = "diff", quiet: bool = False) -> None:
        if direction == "push":
            self._sync_push(conflict=conflict, quiet=quiet)
            return
        if direction == "pull":
            self._sync_pull(conflict=conflict, quiet=quiet)
            return
        raise ValueError(f"Unsupported direction: {direction}")

    def _sync_push(self, conflict: str, quiet: bool) -> None:
        tasks = self.cache.list_tasks()
        dirty = [task for task in tasks if bool(task.get("dirty"))]
        if not dirty:
            if not quiet:
                print("ℹ️ no dirty tasks to push")
            return
        for task in dirty:
            self.write_task(task)
        if not quiet:
            print(f"✅ pushed {len(dirty)} dirty task(s)")

    def _sync_pull(self, conflict: str, quiet: bool) -> None:
        remote = {task.get("id"): task for task in self._list_tasks_remote() if isinstance(task, dict)}
        local_tasks = {task.get("id"): task for task in self.cache.list_tasks() if isinstance(task, dict)}
        for task_id, remote_task in remote.items():
            if not task_id:
                continue
            local_task = local_tasks.get(task_id)
            if local_task and bool(local_task.get("dirty")):
                if self._tasks_differ(local_task, remote_task):
                    self._handle_conflict(task_id, local_task, remote_task, conflict)
                    continue
                local_task["dirty"] = False
                self._cache_task(local_task, dirty=False)
                continue
            self._cache_task(remote_task, dirty=False)
        if not quiet:
            print(f"✅ pulled {len(remote)} task(s)")

    def _handle_conflict(self, task_id: str, local_task: Dict[str, object], remote_task: Dict[str, object], conflict: str) -> None:
        if conflict == "prefer-local":
            self.write_task(local_task)
            return
        if conflict == "prefer-remote":
            self._cache_task(remote_task, dirty=False)
            return
        diff = self._diff_tasks(local_task, remote_task)
        if conflict == "diff":
            print(diff)
            raise RuntimeError(f"Conflict detected for {task_id}")
        raise RuntimeError(f"Conflict detected for {task_id}")

    def _diff_tasks(self, local_task: Dict[str, object], remote_task: Dict[str, object]) -> str:
        local_text = json.dumps(local_task, indent=2, sort_keys=True, ensure_ascii=False).splitlines()
        remote_text = json.dumps(remote_task, indent=2, sort_keys=True, ensure_ascii=False).splitlines()
        return "\n".join(
            difflib.unified_diff(remote_text, local_text, fromfile="remote", tofile="local", lineterm="")
        )

    def _tasks_differ(self, local_task: Dict[str, object], remote_task: Dict[str, object]) -> bool:
        return json.dumps(local_task, sort_keys=True) != json.dumps(remote_task, sort_keys=True)

    def _cache_task(self, task: Dict[str, object], dirty: bool) -> None:
        task["dirty"] = dirty
        self.cache.write_task(task)

    def _list_tasks_remote(self) -> List[Dict[str, object]]:
        tasks: List[Dict[str, object]] = []
        offset = 0
        limit = 100
        while True:
            payload = self._request_json(
                "GET",
                "issues.json",
                params={
                    "project_id": self.project_id,
                    "limit": limit,
                    "offset": offset,
                    "status_id": "*",
                },
            )
            issues = payload.get("issues") if isinstance(payload, dict) else None
            if not isinstance(issues, list):
                break
            for issue in issues:
                task = self._issue_to_task(issue)
                if task:
                    tasks.append(task)
            total = payload.get("total_count") if isinstance(payload, dict) else None
            if total is None or offset + limit >= int(total):
                break
            offset += limit
        return tasks

    def _find_issue_by_task_id(self, task_id: str) -> Optional[Dict[str, object]]:
        issues = self._list_tasks_remote()
        for task in issues:
            if task.get("id") == task_id:
                issue_id = task.get("redmine_id")
                if issue_id:
                    return self._request_json("GET", f"issues/{issue_id}.json").get("issue")
        return None

    def _issue_to_task(self, issue: Dict[str, object]) -> Optional[Dict[str, object]]:
        if not isinstance(issue, dict):
            return None
        task_id = self._custom_field_value(issue, self.custom_fields.get("task_id"))
        id_source = "custom"
        if not task_id:
            task_id = issue.get("id")
            id_source = "redmine"
        if not task_id:
            return None
        status_id = ((issue.get("status") or {}).get("id") if isinstance(issue.get("status"), dict) else None)
        status = self._reverse_status_map.get(int(status_id)) if isinstance(status_id, int) else "TODO"
        verify_val = self._custom_field_value(issue, self.custom_fields.get("verify"))
        commit_val = self._custom_field_value(issue, self.custom_fields.get("commit"))
        task = {
            "id": str(task_id),
            "title": str(issue.get("subject") or ""),
            "description": str(issue.get("description") or ""),
            "status": status or "TODO",
            "priority": str((issue.get("priority") or {}).get("name") or ""),
            "owner": str((issue.get("assigned_to") or {}).get("name") or ""),
            "tags": [tag.get("name") for tag in issue.get("tags", []) if isinstance(tag, dict)],
            "depends_on": [],
            "verify": self._maybe_parse_json(verify_val),
            "commit": self._maybe_parse_json(commit_val),
            "comments": [],
            "redmine_id": issue.get("id"),
            "id_source": id_source,
        }
        return task

    def _task_to_issue_payload(self, task: Dict[str, object]) -> Dict[str, object]:
        status = str(task.get("status") or "").strip().upper()
        payload: Dict[str, object] = {
            "subject": str(task.get("title") or ""),
            "description": str(task.get("description") or ""),
        }
        if status and isinstance(self.status_map, dict) and status in self.status_map:
            payload["status_id"] = self.status_map[status]
        priority = task.get("priority")
        if isinstance(priority, int):
            payload["priority_id"] = priority
        if self.assignee_id:
            payload["assigned_to_id"] = self.assignee_id
        start_date = self._start_date_from_task_id(str(task.get("id") or ""))
        if start_date:
            payload["start_date"] = start_date
        done_ratio = self._done_ratio_for_status(status)
        if done_ratio is not None:
            payload["done_ratio"] = done_ratio
        custom_fields: List[Dict[str, object]] = []
        self._append_custom_field(custom_fields, "task_id", task.get("id"))
        self._append_custom_field(custom_fields, "verify", task.get("verify"))
        self._append_custom_field(custom_fields, "commit", task.get("commit"))
        if custom_fields:
            payload["custom_fields"] = custom_fields
        return payload

    def _append_custom_field(self, fields: List[Dict[str, object]], key: str, value: object) -> None:
        field_id = None
        if isinstance(self.custom_fields, dict):
            field_id = self.custom_fields.get(key)
        if not field_id:
            return
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        fields.append({"id": field_id, "value": value})

    def _start_date_from_task_id(self, task_id: str) -> Optional[str]:
        if not task_id or "-" not in task_id:
            return None
        prefix = task_id.split("-", 1)[0]
        if len(prefix) < 8 or not prefix[:8].isdigit():
            return None
        year = prefix[0:4]
        month = prefix[4:6]
        day = prefix[6:8]
        return f"{year}-{month}-{day}"

    def _done_ratio_for_status(self, status: str) -> Optional[int]:
        if not status:
            return None
        if status == "DONE":
            return 100
        return 0

    def _custom_field_value(self, issue: Dict[str, object], field_id: object) -> Optional[str]:
        if not field_id:
            return None
        fields = issue.get("custom_fields")
        if not isinstance(fields, list):
            return None
        for field in fields:
            if isinstance(field, dict) and field.get("id") == field_id:
                return str(field.get("value") or "")
        return None

    def _maybe_parse_json(self, value: Optional[str]) -> object:
        if value is None:
            return None
        raw = str(value).strip()
        if not raw:
            return None
        if raw.startswith("{") or raw.startswith("["):
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return raw
        return raw

    def _request_json(self, method: str, path: str, payload: Optional[Dict[str, object]] = None, params: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if params:
            url += "?" + urlparse.urlencode(params)
        data = json.dumps(payload).encode("utf-8") if payload else None
        req = urlrequest.Request(
            url,
            data=data,
            method=method,
            headers={
                "Content-Type": "application/json",
                "X-Redmine-API-Key": self.api_key,
            },
        )
        try:
            with urlrequest.urlopen(req, timeout=10) as resp:
                raw = resp.read()
        except urlerror.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)
            raise RuntimeError(f"Redmine API error: {exc.code} {body}") from exc
        except urlerror.URLError as exc:
            raise RedmineUnavailable("Redmine unavailable") from exc
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}
