from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

import yaml


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)")
OBSIDIAN_LINK_RE = re.compile(r"!\[\[([^\]]+)\]\]")


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


def strip_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text
    return text[match.end():]


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


def is_external_reference(ref: str) -> bool:
    lowered = ref.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("tel:")
        or lowered.startswith("#")
    )


def normalize_link_target(ref: str) -> str:
    cleaned = ref.strip()
    cleaned = cleaned.split("#", 1)[0]
    cleaned = cleaned.split("?", 1)[0]
    if "|" in cleaned:
        cleaned = cleaned.split("|", 1)[0]
    return cleaned.strip()


def extract_asset_references(markdown_path: Path) -> list[str]:
    text = markdown_path.read_text(encoding="utf-8")
    body = strip_frontmatter(text)
    refs: list[str] = []

    for match in MARKDOWN_LINK_RE.finditer(body):
        ref = match.group(1) or match.group(2) or ""
        ref = normalize_link_target(ref)
        if not ref or is_external_reference(ref):
            continue
        refs.append(ref)

    for match in OBSIDIAN_LINK_RE.finditer(body):
        ref = normalize_link_target(match.group(1))
        if not ref or is_external_reference(ref):
            continue
        refs.append(ref)

    deduped: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if ref in seen:
            continue
        seen.add(ref)
        deduped.append(ref)
    return deduped


def rewrite_asset_links_for_quartz(markdown_path: Path, content_root: Path) -> bool:
    text = markdown_path.read_text(encoding="utf-8")
    changed = False

    def asset_url(ref: str) -> str | None:
        normalized = normalize_link_target(ref)
        if not normalized or is_external_reference(normalized):
            return None
        resolved = (markdown_path.parent / normalized).resolve()
        try:
            resolved.relative_to(content_root.resolve())
        except ValueError:
            return None
        if not resolved.is_file() or resolved.suffix.lower() == ".md":
            return None
        return "/" + resolved.relative_to(content_root.resolve()).as_posix()

    def replace_markdown(match: re.Match[str]) -> str:
        nonlocal changed
        original = match.group(0)
        ref = match.group(1) or match.group(2) or ""
        url = asset_url(ref)
        if not url:
            return original
        changed = True
        return original.replace(ref, url, 1)

    def replace_obsidian(match: re.Match[str]) -> str:
        nonlocal changed
        ref = match.group(1)
        url = asset_url(ref)
        if not url:
            return match.group(0)
        changed = True
        return f"![]({url})"

    rewritten = MARKDOWN_LINK_RE.sub(replace_markdown, text)
    rewritten = OBSIDIAN_LINK_RE.sub(replace_obsidian, rewritten)

    if changed:
        markdown_path.write_text(rewritten, encoding="utf-8")

    return changed


def markdown_references_asset(markdown_path: Path, asset_path: Path) -> bool:
    for ref in extract_asset_references(markdown_path):
        resolved = (markdown_path.parent / ref).resolve()
        if resolved == asset_path:
            return True
    return False


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


def collect_all_markdown_files(docs_root: Path) -> list[Path]:
    return sorted(path for path in docs_root.rglob("*.md") if path.is_file())


def resolve_changed_markdown_files(docs_root: Path, changed: list[str]) -> list[Path]:
    repo_root = docs_root.parent.resolve()
    all_markdown = collect_all_markdown_files(docs_root)
    selected: set[Path] = set()

    for item in changed:
        changed_path = (Path.cwd() / item).resolve()

        if changed_path == (docs_root / "docs.config.yaml").resolve():
            return all_markdown

        if changed_path.suffix.lower() == ".md":
            try:
                changed_path.relative_to(docs_root)
            except ValueError:
                continue
            selected.add(changed_path)
            continue

        try:
            changed_path.relative_to(repo_root)
        except ValueError:
            continue

        for markdown_path in all_markdown:
            if markdown_references_asset(markdown_path, changed_path):
                selected.add(markdown_path)

    return sorted(selected)


def collect_markdown_files(docs_root: Path, changed: list[str] | None = None) -> list[Path]:
    if changed:
        return resolve_changed_markdown_files(docs_root, changed)
    return collect_all_markdown_files(docs_root)


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
