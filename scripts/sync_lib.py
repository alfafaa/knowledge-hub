from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

import yaml


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1)) or {}
    return data if isinstance(data, dict) else {}


def matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatch(path, pattern)


def best_match(path: str, mapping: dict[str, Any]) -> tuple[str, Any] | None:
    matched = [(pattern, value) for pattern, value in mapping.items() if matches(path, pattern)]
    if not matched:
        return None
    matched.sort(key=lambda item: len(item[0]), reverse=True)
    return matched[0]


def infer_prefix(pattern: str) -> str:
    specials = ["**", "*", "?", "["]
    cut = len(pattern)
    for token in specials:
        idx = pattern.find(token)
        if idx != -1:
            cut = min(cut, idx)
    return pattern[:cut]


def compute_sync_plan(rel_path: str, frontmatter: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    sync = config.get("sync", {})
    defaults = config.get("defaults", {})

    included = any(matches(rel_path, pattern) for pattern in sync.get("include", []))
    excluded = any(matches(rel_path, pattern) for pattern in sync.get("exclude", []))
    if not included or excluded:
        return {
            "source": rel_path,
            "action": "skip",
            "reason": "not included" if not included else "excluded",
        }

    override_match = best_match(rel_path, sync.get("overrides", {}))
    destination_match = best_match(rel_path, sync.get("destinations", {}))

    resolved: dict[str, Any] = {
        "sync_mode": defaults.get("sync_mode"),
        "visibility": defaults.get("visibility"),
        "audience": defaults.get("audience"),
        "publish": defaults.get("publish"),
        "publish_targets": list(defaults.get("publish_targets", [])),
    }

    if override_match:
        resolved.update(override_match[1])

    for field in (
        "sync_mode",
        "visibility",
        "audience",
        "publish",
        "publish_targets",
        "product",
        "project",
        "hub_path",
    ):
        if field in frontmatter:
            resolved[field] = frontmatter[field]

    hub_path = resolved.get("hub_path")
    matched_pattern = None
    if hub_path:
        matched_pattern = "<frontmatter>"
    elif destination_match:
        matched_pattern = destination_match[0]
        hub_path = destination_match[1].get("hub_path")
        for field in ("product", "project", "domain", "publish_targets", "visibility", "audience"):
            if field in destination_match[1] and field not in frontmatter:
                resolved[field] = destination_match[1][field]

    destination_path = None
    if hub_path:
        if matched_pattern == "<frontmatter>":
            relative_suffix = Path(rel_path).name
        else:
            prefix = infer_prefix(matched_pattern or "")
            relative_suffix = rel_path[len(prefix):] if rel_path.startswith(prefix) else rel_path
        destination_path = str(Path(hub_path) / relative_suffix)

    return {
        "source": rel_path,
        "action": resolved.get("sync_mode") or "unknown",
        "publish": resolved.get("publish"),
        "visibility": resolved.get("visibility"),
        "audience": resolved.get("audience"),
        "publish_targets": resolved.get("publish_targets", []),
        "product": resolved.get("product"),
        "project": resolved.get("project"),
        "matched_destination": matched_pattern,
        "destination": destination_path,
    }


def collect_markdown_files(docs_root: Path, changed: list[str] | None = None) -> list[Path]:
    if changed:
        return [(Path.cwd() / item).resolve() for item in changed]
    return sorted(path for path in docs_root.rglob("*.md") if path.is_file())


def compute_plans(docs_root: Path, config: dict[str, Any], changed: list[str] | None = None) -> list[dict[str, Any]]:
    plans: list[dict[str, Any]] = []
    for abs_path in collect_markdown_files(docs_root, changed):
        rel_path = abs_path.relative_to(docs_root.parent).as_posix()
        frontmatter = parse_frontmatter(abs_path) if abs_path.exists() and abs_path.suffix.lower() == ".md" else {}
        plans.append(compute_sync_plan(rel_path, frontmatter, config))
    return plans


def dump_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
