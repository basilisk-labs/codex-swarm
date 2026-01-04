from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


FRONTMATTER_BOUNDARY = "---"
DEFAULT_TASKS_DIR = Path(".codex-swarm/tasks")


@dataclass
class FrontmatterDoc:
    frontmatter: Dict[str, object]
    body: str


def _split_top_level(value: str, sep: str = ",") -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    quote: Optional[str] = None
    for ch in value:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("\"", "'"):
            buf.append(ch)
            quote = ch
            continue
        if ch in "[{(":
            depth += 1
            buf.append(ch)
            continue
        if ch in "]})":
            depth = max(0, depth - 1)
            buf.append(ch)
            continue
        if ch == sep and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    if buf:
        parts.append("".join(buf).strip())
    return [p for p in parts if p]


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("\"", "'"):
        return value[1:-1]
    return value


def _parse_scalar(value: str) -> object:
    raw = value.strip()
    if not raw:
        return ""
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    if raw[0] in ("\"", "'") and raw[-1] == raw[0]:
        return _strip_quotes(raw)
    if raw.isdigit():
        return int(raw)
    return raw


def _parse_inline_list(value: str) -> List[object]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    items = _split_top_level(inner)
    return [_parse_scalar(item) for item in items]


def _parse_inline_dict(value: str) -> Dict[str, object]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return {}
    entries = _split_top_level(inner)
    result: Dict[str, object] = {}
    for entry in entries:
        if ":" not in entry:
            continue
        key, raw_val = entry.split(":", 1)
        key = _strip_quotes(key.strip())
        result[key] = _parse_value(raw_val.strip())
    return result


def _parse_value(value: str) -> object:
    raw = value.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return _parse_inline_list(raw)
    if raw.startswith("{") and raw.endswith("}"):
        return _parse_inline_dict(raw)
    return _parse_scalar(raw)


def parse_frontmatter(text: str) -> FrontmatterDoc:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        return FrontmatterDoc(frontmatter={}, body=text)
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == FRONTMATTER_BOUNDARY:
            end_idx = idx
            break
    if end_idx is None:
        return FrontmatterDoc(frontmatter={}, body=text)
    frontmatter_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    frontmatter = _parse_frontmatter_lines(frontmatter_lines)
    return FrontmatterDoc(frontmatter=frontmatter, body=body)


def _parse_frontmatter_lines(lines: Iterable[str]) -> Dict[str, object]:
    data: Dict[str, object] = {}
    current_list_key: Optional[str] = None
    for raw_line in lines:
        if not raw_line.strip():
            continue
        if raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith("  - ") and current_list_key:
            item_text = raw_line.strip()[2:].strip()
            if item_text.startswith("{") and item_text.endswith("}"):
                item = _parse_inline_dict(item_text)
            else:
                item = _parse_value(item_text)
            current = data.get(current_list_key)
            if isinstance(current, list):
                current.append(item)
            else:
                data[current_list_key] = [item]
            continue
        current_list_key = None
        if ":" not in raw_line:
            continue
        key, raw_val = raw_line.split(":", 1)
        key = key.strip()
        value = raw_val.strip()
        if not value:
            data[key] = []
            current_list_key = key
            continue
        data[key] = _parse_value(value)
    return data


def _format_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    return json.dumps(text, ensure_ascii=False)


def _format_inline_list(values: List[object]) -> str:
    return "[" + ", ".join(_format_scalar(v) for v in values) + "]"


def _format_inline_dict(values: Dict[str, object]) -> str:
    parts = []
    for key, value in values.items():
        parts.append(f"{key}: {_format_scalar(value)}")
    return "{ " + ", ".join(parts) + " }"


def format_frontmatter(frontmatter: Dict[str, object]) -> str:
    lines: List[str] = [FRONTMATTER_BOUNDARY]
    keys = [
        "id",
        "title",
        "status",
        "priority",
        "owner",
        "depends_on",
        "tags",
        "verify",
        "commit",
        "comments",
        "created_at",
    ]
    remaining = [k for k in frontmatter.keys() if k not in keys]
    ordered_keys = keys + sorted(remaining)
    for key in ordered_keys:
        if key not in frontmatter:
            continue
        value = frontmatter[key]
        if isinstance(value, list):
            if value and all(isinstance(item, dict) for item in value):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {_format_inline_dict(item)}")
            else:
                lines.append(f"{key}: {_format_inline_list(value)}")
            continue
        if isinstance(value, dict):
            lines.append(f"{key}: {_format_inline_dict(value)}")
            continue
        lines.append(f"{key}: {_format_scalar(value)}")
    lines.append(FRONTMATTER_BOUNDARY)
    return "\n".join(lines)


class LocalBackend:
    def __init__(self, settings: Optional[Dict[str, object]] = None) -> None:
        raw_dir = (settings or {}).get("dir") if isinstance(settings, dict) else None
        if raw_dir:
            self.root = Path(str(raw_dir)).resolve()
        else:
            self.root = DEFAULT_TASKS_DIR.resolve()

    def task_dir(self, task_id: str) -> Path:
        return self.root / task_id

    def task_readme_path(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "README.md"

    def list_tasks(self) -> List[Dict[str, object]]:
        if not self.root.exists():
            return []
        tasks: List[Dict[str, object]] = []
        for entry in sorted(self.root.iterdir()):
            if not entry.is_dir():
                continue
            readme = entry / "README.md"
            if not readme.exists():
                continue
            doc = parse_frontmatter(readme.read_text(encoding="utf-8"))
            if doc.frontmatter:
                tasks.append(doc.frontmatter)
        return tasks

    def get_task(self, task_id: str) -> Optional[Dict[str, object]]:
        readme = self.task_readme_path(task_id)
        if not readme.exists():
            return None
        doc = parse_frontmatter(readme.read_text(encoding="utf-8"))
        return doc.frontmatter

    def write_task(self, task: Dict[str, object]) -> None:
        task_id = str(task.get("id") or "").strip()
        if not task_id:
            raise ValueError("Task id is required")
        readme = self.task_readme_path(task_id)
        body = ""
        if readme.exists():
            doc = parse_frontmatter(readme.read_text(encoding="utf-8"))
            body = doc.body
        readme.parent.mkdir(parents=True, exist_ok=True)
        frontmatter_text = format_frontmatter(task)
        content = frontmatter_text + "\n"
        if body:
            content += body.lstrip("\n") + "\n"
        readme.write_text(content, encoding="utf-8")

    def export_tasks_json(self, output_path: Path) -> None:
        tasks = self.list_tasks()
        payload = {"tasks": tasks}
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
